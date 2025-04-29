import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import yaml
import numpy as np

class InteractiveRectangleDrawer:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.ax.set_title("Click and drag to draw rectangles\nRight-click on rectangle to delete")
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 10)
        self.ax.grid(True)
        
        self.rectangles = {}
        self.current_rect = None
        self.start_point = None
        self.rect_id = 1
        
        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        
        self.info_text = self.ax.text(0.02, 0.98, "Rectangle info will appear here", 
                                    transform=self.ax.transAxes,
                                    verticalalignment='top',
                                    bbox=dict(facecolor='white', alpha=0.7))
        
        plt.tight_layout()
    
    def on_press(self, event):
        if event.inaxes != self.ax:
            return
        
        if event.button == 1:
            self.start_point = (float(event.xdata), float(event.ydata))
            self.current_rect = {
                'rect': None,
                'start': self.start_point,
                'name': f'rect_{self.rect_id}',
                'color': [float(c) for c in np.random.rand(3)]
            }
            self.rect_id += 1
        
        elif event.button == 3:
            for name, rect_data in list(self.rectangles.items()):
                if rect_data['patch'].contains_point((event.x, event.y)):
                    rect_data['patch'].remove()
                    del self.rectangles[name]
                    self.update_info()
                    self.fig.canvas.draw()
                    break
    
    def on_motion(self, event):
        if self.current_rect is None or event.inaxes != self.ax:
            return
        
        start_x, start_y = self.current_rect['start']
        end_x, end_y = event.xdata, event.ydata
        
        if self.current_rect['rect'] is not None:
            self.current_rect['rect'].remove()
        
        width = end_x - start_x
        height = end_y - start_y
        rect = Rectangle((start_x, start_y), width, height, 
                        fill=False, color=self.current_rect['color'], 
                        linestyle='--', alpha=0.7)
        self.ax.add_patch(rect)
        self.current_rect['rect'] = rect
        self.fig.canvas.draw()
    
    def on_release(self, event):
        if self.current_rect is None or event.inaxes != self.ax:
            return
        
        start_x, start_y = self.current_rect['start']
        end_x, end_y = event.xdata, event.ydata
        
        if abs(end_x - start_x) < 0.2 or abs(end_y - start_y) < 0.2:
            if self.current_rect['rect'] is not None:
                self.current_rect['rect'].remove()
                self.fig.canvas.draw()
            self.current_rect = None
            return
        
        x0 = min(start_x, end_x)
        y0 = min(start_y, end_y)
        width = abs(end_x - start_x)
        height = abs(end_y - start_y)
        
        rect_patch = Rectangle((x0, y0), width, height, 
                         fill=False, color=self.current_rect['color'],
                         alpha=0.7)
        self.ax.add_patch(rect_patch)
        
        center_x = float(x0 + width / 2)
        center_y = float(y0 + height / 2)
        
        self.rectangles[self.current_rect['name']] = {
            'center': [center_x, center_y],  # Stored as list
            'width': float(width),
            'height': float(height),
            'color': self.current_rect['color'],  # Already a list
            'patch': rect_patch
        }
        
        self.ax.plot(center_x, center_y, 'ro', markersize=4)
        self.current_rect = None
        self.update_info()
        self.fig.canvas.draw()
    
    def update_info(self):
        if not self.rectangles:
            self.info_text.set_text("No rectangles\nLeft-click and drag to draw rectangles")
            return
        
        info_text = "Current rectangles:\n\n"
        for name, rect in self.rectangles.items():
            center_x, center_y = rect['center']
            info_text += (
                f"Name: {name}\n"
                f"Center: [{center_x:.2f}, {center_y:.2f}]\n"
                f"Width: {rect['width']:.2f}, Height: {rect['height']:.2f}\n"
                f"Color: {rect['color']}\n\n"
            )
        
        self.info_text.set_text(info_text)
    
    def save_to_yaml(self, filename):
        data = {}
        for name, rect in self.rectangles.items():
            data[name] = {
                'center': rect['center'],  # Already a list
                'width': float(rect['width']),
                'height': float(rect['height']),
                'color': rect['color']  # Already a list
            }
        
        with open(filename, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
        
        print(f"Rectangle data saved to {filename}")


def main():
    drawer = InteractiveRectangleDrawer()
    
    def on_save(event):
        if not drawer.rectangles:
            print("No rectangles to save!")
            return
        
        default_filename = "rectangles.yaml"
        filename = input(f"Enter filename to save (default: {default_filename}): ") or default_filename
        
        if not filename.lower().endswith(('.yaml', '.yml')):
            filename += '.yaml'
        
        try:
            drawer.save_to_yaml(filename)
            drawer.ax.set_title(f"Rectangles saved to {filename}")
            drawer.fig.canvas.draw()
        except Exception as e:
            print(f"Save failed: {str(e)}")
    
    ax_button = plt.axes([0.8, 0.02, 0.15, 0.05])
    btn_save = plt.Button(ax_button, 'Save to YAML')
    btn_save.on_clicked(on_save)
    
    ax_clear = plt.axes([0.6, 0.02, 0.15, 0.05])
    btn_clear = plt.Button(ax_clear, 'Clear All')
    btn_clear.on_clicked(lambda event: [rect['patch'].remove() for rect in drawer.rectangles.values()] 
                         or drawer.rectangles.clear() 
                         or drawer.update_info() 
                         or drawer.fig.canvas.draw())
    
    plt.show()


if __name__ == "__main__":
    main()