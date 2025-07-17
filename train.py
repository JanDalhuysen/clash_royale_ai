if __name__ == '__main__':
    from multiprocessing import freeze_support
    freeze_support()

    from ultralytics import YOLO

    # Load a model from a file
    model = YOLO('yolov8n.pt')

    train_path = './train/images'
    val_path = './val/images'
    test_path = './test/images'

    # Fine-tune the model
    results = model.train(
        data='data.yaml',
        epochs=64
    )
