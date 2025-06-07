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
        epochs=100
    )

    # Install the ultralytics package using conda
    # conda install -c conda-forge ultralytics

    # C:\Users\dalhu\AppData\Roaming\Ultralytics

    # https://prod.liveshare.vsengsaas.visualstudio.com/join?86DDE4FD23CB767DF5317A3D80BC7F7F170D
    # is in '/home/27976882/.config/Ultralytics/settings.yaml'
