# ai/training/optimized_trainer.py
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2  # Lighter and faster
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
import json
import os
import matplotlib.pyplot as plt
from datetime import datetime

class OptimizedPlantTrainer:
    def __init__(self, dataset_path="data/raw/PlantVillage"):
        self.dataset_path = dataset_path
        self.img_height = 224
        self.img_width = 224
        self.batch_size = 32
        self.model = None
        self.history = None
        
    def prepare_data(self):
        """Prepare data with optimal augmentation for plant diseases"""
        print("📊 Preparing training data...")
        
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=25,  # Increased for plant leaves
            width_shift_range=0.2,
            height_shift_range=0.2,
            horizontal_flip=True,
            vertical_flip=True,  # Added for leaves
            zoom_range=0.3,  # Increased for close-up leaves
            brightness_range=[0.8, 1.2],  # Lighting variations
            channel_shift_range=0.2,  # Color variations
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
    
    def create_lightweight_model(self, num_classes):
        """Create MobileNetV2 model - faster training and good accuracy"""
        print("🧠 Creating MobileNetV2 model...")
        
        # Load pre-trained MobileNetV2 (lighter than EfficientNet)
        base_model = MobileNetV2(
            weights='imagenet',
            include_top=False,
            input_shape=(self.img_height, self.img_width, 3)
        )
        
        # Freeze base model initially
        base_model.trainable = False
        
        # Add custom layers
        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = Dense(256, activation='relu')(x)
        x = Dropout(0.3)(x)
        x = Dense(128, activation='relu')(x)
        x = Dropout(0.2)(x)
        predictions = Dense(num_classes, activation='softmax')(x)
        
        model = Model(inputs=base_model.input, outputs=predictions)
        
        # Compile model
        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        print("✅ Lightweight model created!")
        return model
    
    def train_fast(self, epochs=15):
        """Fast training optimized for your dataset"""
        print("🚀 Starting optimized training...")
        
        # Prepare data
        train_gen, val_gen = self.prepare_data()
        num_classes = len(train_gen.class_indices)
        
        # Create model
        self.model = self.create_lightweight_model(num_classes)
        
        # Callbacks for efficient training
        callbacks = [
            ModelCheckpoint(
                'ai/models/best_plant_model.h5',
                monitor='val_accuracy',
                save_best_only=True,
                mode='max',
                verbose=1
            ),
            EarlyStopping(
                monitor='val_accuracy',
                patience=8,  # Stop if no improvement for 8 epochs
                restore_best_weights=True,
                verbose=1
            ),
            ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,  # Reduce learning rate by half
                patience=3,
                min_lr=1e-7,
                verbose=1
            )
        ]
        
        print("📚 Phase 1: Training with frozen base (5 epochs)...")
        history1 = self.model.fit(
            train_gen,
            epochs=5,
            validation_data=val_gen,
            callbacks=callbacks,
            verbose=1,
            steps_per_epoch=min(100, len(train_gen)),  # Limit steps for speed
            validation_steps=min(50, len(val_gen))
        )
        
        print("🎯 Phase 2: Fine-tuning (10 epochs)...")
        # Unfreeze some layers for fine-tuning
        base_model = self.model.layers[0]
        base_model.trainable = True
        
        # Fine-tune from this layer onwards
        fine_tune_at = len(base_model.layers) // 2
        
        for layer in base_model.layers[:fine_tune_at]:
            layer.trainable = False
        
        # Recompile with lower learning rate
        self.model.compile(
            optimizer=Adam(learning_rate=0.0001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        history2 = self.model.fit(
            train_gen,
            epochs=epochs,
            validation_data=val_gen,
            callbacks=callbacks,
            initial_epoch=5,
            verbose=1,
            steps_per_epoch=min(150, len(train_gen)),
            validation_steps=min(50, len(val_gen))
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
        
        print("✅ Class names saved!")
        
        return self.history
    
    def evaluate_model(self, validation_generator):
        """Evaluate the trained model"""
        print("📊 Evaluating model...")
        
        loss, accuracy = self.model.evaluate(validation_generator)
        print(f"✅ Final Validation Accuracy: {accuracy:.4f}")
        print(f"✅ Final Validation Loss: {loss:.4f}")
        
        return accuracy, loss

def main():
    # Create directories
    os.makedirs('ai/models', exist_ok=True)
    
    print("🌱 LeGeberew AI Model Training")
    print("=" * 40)
    
    # Initialize and train
    trainer = OptimizedPlantTrainer()
    history = trainer.train_fast(epochs=15)
    
    # Evaluate
    _, val_gen = trainer.prepare_data()
    accuracy, loss = trainer.evaluate_model(val_gen)
    
    print("\n🎉 Training Completed!")
    print(f"📈 Final Accuracy: {accuracy:.2%}")
    print(f"📉 Final Loss: {loss:.4f}")
    print("\n📁 Model files created:")
    print("   - ai/models/final_plant_model.h5")
    print("   - ai/models/best_plant_model.h5") 
    print("   - ai/models/class_names.json")

if __name__ == "__main__":
    main()