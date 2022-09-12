import os

import mlflow
import tensorflow as tf
from tensorflow import keras
from mlflow.tracking import MlflowClient
from mlflow.exceptions import RestException

class_labels = {
    0: 'Speed limit (20km/h)',
    1: 'Speed limit (30km/h)',
    2: 'Speed limit (50km/h)',
    3: 'Speed limit (60km/h)',
    4: 'Speed limit (70km/h)',
    5: 'Speed limit (80km/h)',
    6: 'End of speed limit (80km/h)',
    7: 'Speed limit (100km/h)',
    8: 'Speed limit (120km/h)',
    9: 'No passing',
    10: 'No passing veh over 3.5 tons',
    11: 'Right-of-way at intersection',
    12: 'Priority road',
    13: 'Yield',
    14: 'Stop',
    15: 'No vehicles',
    16: 'Veh > 3.5 tons prohibited',
    17: 'No entry',
    18: 'General caution',
    19: 'Dangerous curve left',
    20: 'Dangerous curve right',
    21: 'Double curve',
    22: 'Bumpy road',
    23: 'Slippery road',
    24: 'Road narrows on the right',
    25: 'Road work',
    26: 'Traffic signals',
    27: 'Pedestrians',
    28: 'Children crossing',
    29: 'Bicycles crossing',
    30: 'Beware of ice/snow',
    31: 'Wild animals crossing',
    32: 'End speed + passing limits',
    33: 'Turn right ahead',
    34: 'Turn left ahead',
    35: 'Ahead only',
    36: 'Go straight or right',
    37: 'Go straight or left',
    38: 'Keep right',
    39: 'Keep left',
    40: 'Roundabout mandatory',
    41: 'End of no passing',
    42: 'End no passing veh > 3.5 tons',
}


# ## Loading datasets

BASE_PATH = '../data/GTSRB'
TRAIN_PATH = BASE_PATH + '/Training'
TEST_PATH = BASE_PATH + '/Online-Test-sort'

BATCH_SIZE = 8
IMAGE_SIZE = 150


train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    samplewise_center=False,
    samplewise_std_normalization=False,
    rotation_range=0.1,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.1,
    zoom_range=0.1,
    cval=0.0,
    rescale=1.0 / 255,
    validation_split=0.2,
)

train_generator = train_datagen.flow_from_directory(
    TRAIN_PATH,
    target_size=(IMAGE_SIZE, IMAGE_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    seed=123,
    subset="training",
)

validation_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    samplewise_center=False,
    samplewise_std_normalization=False,
    rescale=1.0 / 255,
    validation_split=0.2,
)

validation_generator = validation_datagen.flow_from_directory(
    TRAIN_PATH,
    target_size=(IMAGE_SIZE, IMAGE_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    seed=123,
    subset="validation",
)


# ## Building Network

# base_model = tf.keras.applications.EfficientNetB0(
base_model = tf.keras.applications.ResNet152V2(
    include_top=False,
    weights="imagenet",
    input_shape=(IMAGE_SIZE, IMAGE_SIZE, 3),
    pooling=None,
    classes=len(class_labels),
    classifier_activation="softmax",
)

model_name = base_model.name

base_model.trainable = False
base_model.summary()


inputs = keras.Input(shape=(IMAGE_SIZE, IMAGE_SIZE, 3))
# We make sure that the base_model is running in inference mode here,
# by passing `training=False`. This is important for fine-tuning, as you will
# learn in a few paragraphs.
x = base_model(inputs, training=False)
# Convert features of shape `base_model.output_shape[1:]` to vectors
x = keras.layers.GlobalAveragePooling2D()(x)
# A Dense classifier with a single unit (binary classification)
outputs = keras.layers.Dense(len(class_labels))(x)
model = keras.Model(inputs, outputs)

model.compile(
    optimizer=keras.optimizers.Adam(),
    loss=keras.losses.CategoricalCrossentropy(from_logits=True),
    metrics=["accuracy"],
)


early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor="val_loss",
    min_delta=1e-4,
    patience=4,
)

reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(
    monitor="val_loss",
    factor=0.1,
    patience=2,
    min_delta=1e-4,
    min_lr=0.001,
)


# ## Training and Testing

test_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    samplewise_center=False,
    samplewise_std_normalization=False,
    rescale=1.0 / 255,
    validation_split=0.2,
)

test_generator = validation_datagen.flow_from_directory(
    TEST_PATH,
    target_size=(IMAGE_SIZE, IMAGE_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
)

mlflow_address = os.getenv(MLFLOW_URL, "http://localhost:5000/")
mlflow_uri = "http://" + mlflow_address + ":5000/"
mlflow.set_tracking_uri(mlflow_uri)
mlflow.set_experiment("road-signs-recognition")


mlflow.tensorflow.autolog()
mlflow.log_param("model", model_name)

model.fit(
    train_generator,
    epochs=5,  # This takes forever to run on cheap EC2 instances so I limited it
    #         verbose=2,
    callbacks=[early_stopping, reduce_lr],
    validation_data=validation_generator,
)

test_loss, test_acc = model.evaluate(test_generator)
print("Test Accuracy:", test_acc)

mlflow.log_metric("test_loss", test_loss)
mlflow.log_metric("test_acc", test_acc)


# ### This doesn't predict that well but I think that's okay for the purposes of this project

# ## Registering Model

client = MlflowClient(mlflow_uri)


client.list_registered_models()


model_name = 'sign-classifier'

try:
    latest_versions = client.get_latest_versions(name=model_name)
except RestException:
    print("Model does not exist yet.")
    latest_versions = []

for version in latest_versions:
    print(f"version: {version.version}, stage: {version.current_stage}")


client.delete_registered_model(name=model_name)


run = mlflow.active_run()
run_id = run.info.run_id

mlflow.register_model(model_uri=f"runs:/{run_id}/model", name='sign-classifier')


# ## Promoting model if test accuracy is better

# If no model, set current as Production
if len(latest_versions) < 1:
    client.transition_model_version_stage(
        name=model_name, version=1, stage="Production", archive_existing_versions=True
    )
else:
    # Gets prod model to compare
    prod_model = mlflow.pyfunc.load_model(f"models:/{model_name}/Production")
    print(prod_model.metadata)

    prod_model_run = mlflow.get_run(run_id=prod_model.metadata.run_id)
    prod_model_metrics = prod_model_run.data.metrics
    print(f"metrics: {prod_model_metrics}")

    # If new test accuracy is higher, set current model as production model
    if test_acc > prod_model_metrics.get('test_acc'):
        version = len(latest_versions) + 1
        print(version)
        client.transition_model_version_stage(
            name=model_name,
            version=version,
            stage="Production",
            archive_existing_versions=True,
        )
