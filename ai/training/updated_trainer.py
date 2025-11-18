# ai/training/updated_trainer.py
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
import json
import os
import matplotlib.pyplot as plt
from datetime import datetime

class UpdatedPlantTrainer:
    def __init__(self, dataset_path="data/raw/PlantVillage"):
        self.dataset_path = dataset_path
        self.img_height = 224
        self.img_width = 224
        self.batch_size = 32
        self.model = None
        self.history = None
        
    def prepare_data(self):
        """Prepare data with optimal augmentation"""
        print("📊 Preparing training data...")
        
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=25,
            width_shift_range=0.2,
            height_shift_range=0.2,
            horizontal_flip=True,
            vertical_flip=True,
            zoom_range=0.3,
            brightness_range=[0.8, 1.2],
            fill_mode='nearest',
            validation_split=0.2
        )
        
        train_generator = train_datagen.flow_from_directory(
            self.dataset_path,
            target_size=(self.img_height, self.img_width),
            batch_size=self.batch_size,
            class_mode='categorical',
            subset='training',
            shuffle=True
        )
        
        validation_generator = train_datagen.flow_from_directory(
            self.dataset_path,
            target_size=(self.img_height, self.img_width),
            batch_size=self.batch_size,
            class_mode='categorical',
            subset='validation',
            shuffle=False
        )
        
        print(f"✅ Training samples: {train_generator.samples}")
        print(f"✅ Validation samples: {validation_generator.samples}")
        print(f"✅ Number of classes: {len(train_generator.class_indices)}")
        print("📝 Classes:", list(train_generator.class_indices.keys()))
        
        return train_generator, validation_generator
    
    def create_model(self, num_classes):
        """Create MobileNetV2 model for plant disease classification"""
        print("🧠 Creating MobileNetV2 model...")
        
        # Load pre-trained MobileNetV2
        base_model = MobileNetV2(
            weights='imagenet',
            include_top=False,
            input_shape=(self.img_height, self.img_width, 3)
        )
        
        # Freeze base model initially
        base_model.trainable = False
        
        # Build model
        inputs = tf.keras.Input(shape=(self.img_height, self.img_width, 3))
        x = base_model(inputs, training=False)
        x = GlobalAveragePooling2D()(x)
        x = Dense(256, activation='relu')(x)
        x = Dropout(0.3)(x)
        x = Dense(128, activation='relu')(x)
        x = Dropout(0.2)(x)
        outputs = Dense(num_classes, activation='softmax')(x)
        
        model = Model(inputs, outputs)
        
        # Compile model
        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy', 'precision', 'recall']
        )
        
        print("✅ Model created successfully!")
        return model
    
    def train(self, epochs=20):
        """Train the model with transfer learning"""
        print("🚀 Starting model training...")
        
        # Prepare data
        train_gen, val_gen = self.prepare_data()
        num_classes = len(train_gen.class_indices)
        
        # Create model
        self.model = self.create_model(num_classes)
        
        # Callbacks
        callbacks = [
            ModelCheckpoint(
                'ai/models/best_model.h5',
                monitor='val_accuracy',
                save_best_only=True,
                mode='max',
                verbose=1
            ),
            EarlyStopping(
                monitor='val_accuracy',
                patience=10,
                restore_best_weights=True,
                verbose=1
            ),
            ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=1e-7,
                verbose=1
            )
        ]
        
        # Phase 1: Train with frozen base
        print("📚 Phase 1: Training with frozen base (10 epochs)...")
        history1 = self.model.fit(
            train_gen,
            epochs=10,
            validation_data=val_gen,
            callbacks=callbacks,
            verbose=1
        )
        
        # Phase 2: Fine-tuning
        print("🎯 Phase 2: Fine-tuning (10 epochs)...")
        
        # Unfreeze the top layers of the base model
        base_model = self.model.layers[1]  # MobileNetV2 is the second layer
        base_model.trainable = True
        
        # Fine-tune from this layer onwards
        fine_tune_at = 100
        
        # Freeze all the layers before the `fine_tune_at` layer
        for layer in base_model.layers[:fine_tune_at]:
            layer.trainable = False
        
        # Recompile with lower learning rate
        self.model.compile(
            optimizer=Adam(learning_rate=0.0001),
            loss='categorical_crossentropy',
            metrics=['accuracy', 'precision', 'recall']
        )
        
        history2 = self.model.fit(
            train_gen,
            initial_epoch=10,
            epochs=epochs,
            validation_data=val_gen,
            callbacks=callbacks,
            verbose=1
        )
        
        # Combine histories
        self.history = {
            'accuracy': history1.history['accuracy'] + history2.history['accuracy'],
            'val_accuracy': history1.history['val_accuracy'] + history2.history['val_accuracy'],
            'loss': history1.history['loss'] + history2.history['loss'],
            'val_loss': history1.history['val_loss'] + history2.history['val_loss']
        }
        
        # Save final model
        self.model.save('ai/models/final_plant_model.h5')
        print("✅ Final model saved: ai/models/final_plant_model.h5")
        
        # Save class indices
        class_indices = train_gen.class_indices
        with open('ai/models/class_names.json', 'w') as f:
            json.dump(class_indices, f, indent=2)
        
        print("✅ Class names saved: ai/models/class_names.json")
        
        return self.history
    
    def evaluate_model(self):
        """Evaluate the trained model"""
        print("📊 Evaluating model...")
        
        _, val_gen = self.prepare_data()
        results = self.model.evaluate(val_gen, verbose=0)
        
        print(f"✅ Final Validation Accuracy: {results[1]:.4f}")
        print(f"✅ Final Validation Loss: {results[0]:.4f}")
        
        return results[1]  # Return accuracy

def main():
    # Create directories
    os.makedirs('ai/models', exist_ok=True)
    
    print("🌱 LeGeberew AI - Real Model Training")
    print("=" * 50)
    
    # Train the model
    trainer = UpdatedPlantTrainer()
    history = trainer.train(epochs=20)
    
    # Evaluate
    accuracy = trainer.evaluate_model()
    
    print(f"\n🎉 Training Completed!")
    print(f"📈 Final Accuracy: {accuracy:.2%}")
    print("\n📁 Model files created:")
    print("   - ai/models/final_plant_model.h5")
    print("   - ai/models/best_model.h5") 
    print("   - ai/models/class_names.json")
    
    print("\n🚀 Your AI model is now ready for real disease detection!")

if __name__ == "__main__":
    main()