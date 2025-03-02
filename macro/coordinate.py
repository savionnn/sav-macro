from pynput import mouse
def coordinate():
    coords = []
    def on_click(x, y, button, pressed):
        if pressed:
            coords.append((x, y)) 
            listener.stop() 
    with mouse.Listener(on_click=on_click) as listener:
        listener.join() 
    return coords[0] if coords else None

        