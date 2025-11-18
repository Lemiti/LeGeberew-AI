# ai/training/model_trainer.py
import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB3
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout, BatchNormalization
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
import json
import os

class AdvancedDiseaseModel:
    def __init__(self, num_classes):
        self.num_classes = num_classes
        self.img_height = 224
        self.img_width = 224
        
    def create_model(self):
        """Create advanced model with transfer learning"""
        # Use EfficientNet for better accuracy
        base_model = EfficientNetB3(
            weights='imagenet',
            include_top=False,
            input_shape=(self.img_height, self.img_width, 3)
        )
        
        # Freeze base model initially
        base_model.trainable = False
        
        # Add custom layers
        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = BatchNormalization()(x)
        x = Dense(512, activation='relu')(x)
        x = Dropout(0.3)(x)
        x = Dense(256, activation='relu')(x)
        x = Dropout(0.2)(x)
        predictions = Dense(self.num_classes, activation='softmax')(x)
        
        model = Model(inputs=base_model.input, outputs=predictions)
        
        # Compile model
        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy', 'precision', 'recall']
        )
        
        return model
    
    def train_model(self, train_generator, validation_generator, epochs=50):
        """Train model with advanced techniques"""
        model = self.create_model()
        
        # Callbacks
        checkpoint = ModelCheckpoint(
            'ai/models/best_model.h5',
            monitor='val_accuracy',
            save_best_only=True,
            mode='max',
            verbose=1
        )
        
        early_stop = EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True,
            verbose=1
        )
        
        reduce_lr = ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.2,
            patience=5,
            min_lr=1e-7,
            verbose=1
        )
        
        # Initial training with frozen base
        print("Phase 1: Training with frozen base layers...")
        history1 = model.fit(
            train_generator,
            epochs=10,
            validation_data=validation_generator,
            callbacks=[checkpoint, early_stop, reduce_lr]
        )
        
        # Fine-tuning
        print("Phase 2: Fine-tuning with unfrozen layers...")
        base_model = model.layers[0]
        base_model.trainable = True
        
        # Recompile with lower learning rate
        model.compile(
            optimizer=Adam(learning_rate=1e-5),
            loss='categorical_crossentropy',
            metrics=['accuracy', 'precision', 'recall']
        )
        
        history2 = model.fit(
            train_generator,
            epochs=epochs,
            validation_data=validation_generator,
            callbacks=[checkpoint, early_stop, reduce_lr],
            initial_epoch=10
        )
        
        # Save final model
        model.save('ai/models/final_disease_model.h5')
        
        # Save class indices
        class_indices = train_generator.class_indices
        with open('ai/models/class_names.json', 'w') as f:
            json.dump(class_indices, f)
        
        return model, {**history1.history, **history2.history}