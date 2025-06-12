# game_api.py
from flask import Flask, jsonify, request
import json

# --- YOLO DETECTION INTEGRATION ---
# Store for current detections
current_detections = {
    "hand": [],
    "my_troops": [],
    "enemy_troops": []
}

# Simple in-memory storage for demonstration
def update_yolo_detections(new_detections):
    """Update the current detections with new data from YOLO model."""
    global current_detections
    current_detections = new_detections
    print("Updated detections:", new_detections)
    return True

def get_yolo_detections():
    """Get the current detections from YOLO model."""
    print("Python: Returning current YOLOv8 detections...")
    return current_detections

def get_game_metrics():
    # In reality, this function would use OCR or other methods.
    print("Python: Reading game metrics (towers, time)...")
    return {
        "my_king_hp": 2400,
        "my_princess_left_hp": 1400,
        "my_princess_right_hp": 1400,
        "enemy_king_hp": 2400,
        "enemy_princess_left_hp": 1400,
        "enemy_princess_right_hp": 0, # One tower is down
        "time_left_seconds": 125
    }

def perform_card_placement(card_name, x, y):
    # In reality, this would use PyAutoGUI or ADB to simulate the click.
    print(f"Python: ACTION! Placing '{card_name}' at ({x}, {y}).")
    # e.g., pyautogui.click(x, y)
    return {"status": "success", "message": f"Placed {card_name} at {x},{y}"}
# --- END MOCKUP FUNCTIONS ---

app = Flask(__name__)

@app.route('/get_game_state', methods=['GET'])
def get_game_state():
    """Endpoint to get all perception data in one call."""
    yolo_data = get_yolo_detections()
    metrics_data = get_game_metrics()
    
    # Combine all data into a single response
    full_state = {**yolo_data, **metrics_data}
    return jsonify(full_state)

@app.route('/update_detections', methods=['POST'])
def update_detections():
    """Endpoint to update detection results from YOLO model."""
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No data provided"}), 400
        
    if update_yolo_detections(data):
        return jsonify({"status": "success", "message": "Detections updated successfully"})
    else:
        return jsonify({"status": "error", "message": "Failed to update detections"}), 500

@app.route('/place_card', methods=['POST'])
def place_card():
    """Endpoint to execute a game action."""
    data = request.get_json()
    card_name = data.get('card_name')
    x = data.get('x')
    y = data.get('y')

    if not all([card_name, isinstance(x, int), isinstance(y, int)]):
        return jsonify({"status": "error", "message": "Invalid input"}), 400
        
    result = perform_card_placement(card_name, x, y)
    return jsonify(result)

if __name__ == '__main__':
    # Use a specific port, e.g., 5000
    app.run(host='0.0.0.0', port=5000)
