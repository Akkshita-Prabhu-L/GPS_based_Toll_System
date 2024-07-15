import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from geopy.distance import geodesic

# Define toll zones with GPS coordinates and names (example toll points in India)
TOLL_ZONES = [
    ((28.613939, 77.209021), 5, "Delhi"),
    ((19.076090, 72.877426), 7, "Mumbai"),
    ((12.971599, 77.594566), 6, "Bangalore"),
    ((13.082680, 80.270718), 5, "Chennai"),
    ((22.572645, 88.363892), 7, "Kolkata"),
    ((26.912434, 75.787270), 4, "Jaipur"),
    ((23.259933, 77.412613), 4, "Bhopal"),
    ((18.520430, 73.856743), 4, "Pune"),
    ((17.385044, 78.486671), 5, "Hyderabad"),
    ((21.170240, 72.831062), 4, "Surat"),
    ((15.317277, 75.713888), 4, "Hubli"),
    ((11.016844, 76.955832), 4, "Coimbatore"),
    ((9.925201, 78.119774), 4, "Madurai"),
    ((15.849695, 74.497674), 4, "Belgaum"),
    ((19.751480, 75.713888), 4, "Aurangabad"),
    ((22.719568, 75.857727), 4, "Indore"),
    ((23.022505, 72.571362), 4, "Ahmedabad"),
    ((24.585445, 73.712479), 4, "Udaipur"),
    ((26.846708, 80.946159), 4, "Lucknow"),
    ((27.023804, 74.217933), 4, "Ajmer"),
    ((29.945690, 78.164247), 4, "Haridwar"),
    ((30.316496, 78.032188), 4, "Dehradun"),
    ((31.104814, 77.173403), 4, "Shimla"),
    ((32.726602, 74.857026), 4, "Jammu"),
    ((34.083656, 74.797371), 4, "Srinagar"),
    ((25.317645, 82.973914), 4, "Varanasi"),
    ((25.594095, 85.137566), 4, "Patna"),
    ((26.449923, 74.639916), 4, "Ajmer"),
    ((28.408912, 77.317789), 4, "Faridabad"),
    ((28.459497, 77.026638), 4, "Gurgaon"),
    ((30.901011, 75.857276), 4, "Ludhiana"),
    ((25.448425, 78.568459), 4, "Jhansi"),
    ((23.610180, 85.279935), 4, "Ranchi"),
    ((23.831457, 91.286778), 4, "Agartala"),
    ((24.800615, 93.950017), 4, "Imphal"),
    ((27.471012, 94.911964), 4, "Dimapur"),
    ((27.176670, 78.008075), 4, "Agra"),
    ((22.719568, 75.857727), 4, "Indore"),
    ((22.307159, 73.181219), 4, "Vadodara"),
    ((21.145800, 79.088155), 4, "Nagpur"),
    ((20.937424, 77.779551), 4, "Amravati"),
    ((19.876165, 75.343314), 4, "Jalna"),
    ((17.686816, 83.218482), 4, "Visakhapatnam"),
    ((16.506174, 80.648015), 4, "Vijayawada"),
    ((15.139393, 76.921443), 4, "Bellary"),
    ((13.628756, 79.419181), 4, "Tirupati"),
    ((12.295810, 76.639381), 4, "Mysore"),
    ((11.941591, 79.808313), 4, "Puducherry"),
    ((10.786999, 78.705566), 4, "Tiruchirappalli"),
    ((9.287625, 76.654793), 4, "Kottayam"),
    ((8.524139, 76.936638), 4, "Thiruvananthapuram"),
    ((26.144518, 91.736237), 4, "Guwahati"),
    ((25.360809, 85.011017), 4, "Bihar Sharif"),
    ((24.412966, 85.323961), 4, "Hazaribagh"),
    ((22.998763, 87.854975), 4, "Durgapur"),
    ((22.572646, 88.363895), 4, "Kolkata"),
    ((20.296059, 85.824540), 4, "Bhubaneswar"),
    ((21.145800, 79.088155), 4, "Nagpur"),
    ((16.994444, 73.300000), 4, "Kolhapur"),
    ((12.971598, 77.594566), 4, "Bangalore"),
    ((10.850516, 76.271083), 4, "Palakkad"),
    ((11.740086, 92.658640), 4, "Port Blair"),
    ((28.669156, 77.453758), 4, "Ghaziabad"),
    ((27.204612, 77.497684), 4, "Mathura"),
    ((25.448425, 78.568459), 4, "Jhansi"),
    ((23.634501, 92.731681), 4, "Aizawl"),
    ((22.806943, 86.202875), 4, "Jamshedpur"),
    ((21.170240, 72.831062), 4, "Surat"),
    ((19.876165, 75.343314), 4, "Jalna"),
    ((18.112437, 79.019301), 4, "Warangal"),
    ((15.828126, 78.037279), 4, "Kadapa"),
    ((13.082680, 80.270718), 4, "Chennai"),
    ((10.991621, 76.961632), 4, "Coimbatore"),
    ((9.939093, 78.121719), 4, "Madurai"),
    ((8.088306, 77.538451), 4, "Nagercoil"),
    ((12.971598, 77.594566), 4, "Bangalore"),
    ((11.127123, 78.656891), 4, "Erode"),
    ((10.167168, 76.641271), 4, "Kottayam"),
    ((8.713912, 77.756652), 4, "Tirunelveli"),
    ((11.108524, 77.341066), 4, "Tiruppur"),
    ((12.971598, 77.594566), 4, "Bangalore"),
    ((12.295810, 76.639381), 4, "Mysore"),
    ((10.850516, 76.271083), 4, "Palakkad"),
]

# Define canvas size
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 800

# Define the mapping from canvas coordinates to GPS coordinates (you'll need to fine-tune this)
def canvas_to_gps(x, y):
    # Map image dimensions
    img_width = 800
    img_height = 800

    # GPS bounds (top-left and bottom-right corners of the map image)
    gps_top_left = (35.0, 68.0)  # Example coordinates
    gps_bottom_right = (5.0, 97.0)  # Example coordinates

    lat = gps_top_left[0] - (y / img_height) * (gps_top_left[0] - gps_bottom_right[0])
    lon = gps_top_left[1] + (x / img_width) * (gps_bottom_right[1] - gps_top_left[1])
    return (lat, lon)

# Convert GPS coordinates to canvas coordinates
def gps_to_canvas(lat, lon):
    # Map image dimensions
    img_width = 800
    img_height = 800

    # GPS bounds (top-left and bottom-right corners of the map image)
    gps_top_left = (35.0, 68.0)  # Example coordinates
    gps_bottom_right = (5.0, 97.0)  # Example coordinates

    x = (lon - gps_top_left[1]) / (gps_bottom_right[1] - gps_top_left[1]) * img_width
    y = (gps_top_left[0] - lat) / (gps_top_left[0] - gps_bottom_right[0]) * img_height
    return (x, y)

class VehicleSelection(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Select Vehicle Type")
        self.geometry("400x200")
        self.resizable(False, False)

        self.vehicle_type_var = tk.StringVar()
        self.vehicle_type_var.set('Select Vehicle Type')

        ttk.Label(self, text="Select Vehicle Type").pack(pady=10)

        self.vehicle_type_menu = ttk.Combobox(self, textvariable=self.vehicle_type_var)
        self.vehicle_type_menu['values'] = [
            'Car/Jeep/Van/LMV',
            'Light Commercial Vehicle/LGV/Mini-Bus',
            'Bus/Truck (2 axles)',
            'Three-axle Commercial Vehicle',
            'Heavy Construction Machinery/Multi-axle (4-6 axles)',
            'Oversized Vehicle (7+ axles)'
        ]
        self.vehicle_type_menu.pack(pady=10)

        self.proceed_button = ttk.Button(self, text="Next", command=self.start_route_selection)
        self.proceed_button.pack(side=tk.LEFT, padx=20, pady=20)

        self.cancel_button = ttk.Button(self, text="Cancel", command=self.destroy)
        self.cancel_button.pack(side=tk.RIGHT, padx=20, pady=20)

    def start_route_selection(self):
        vehicle_type = self.vehicle_type_var.get()
        if vehicle_type == 'Select Vehicle Type' or vehicle_type == '':
            messagebox.showwarning("Select Vehicle Type", "Please select a vehicle type.")
            return
        self.destroy()
        app = TollSimulator(vehicle_type)
        app.mainloop()

class TollSimulator(tk.Tk):
    def __init__(self, vehicle_type):
        super().__init__()
        self.vehicle_type = vehicle_type
        self.title("Toll Road Simulator")
        self.geometry(f"{CANVAS_WIDTH}x{CANVAS_HEIGHT+100}")  # Adjusted window size to fit the image and dropdown

        self.canvas = tk.Canvas(self, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        self.canvas.pack()

        # Load and scale down the map image
        self.map_image = Image.open("C:/Users/akksh/OneDrive/Desktop/india-road-map.gif")
        self.map_image = self.map_image.resize((CANVAS_WIDTH, CANVAS_HEIGHT), Image.LANCZOS)
        self.map_photo = ImageTk.PhotoImage(self.map_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.map_photo)

        self.toll_points = []
        self.route_points = []
        self.hover_label = tk.Label(self, text="", bg="yellow", fg="black")

        for zone in TOLL_ZONES:
            x, y = gps_to_canvas(*zone[0])
            point = self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="blue", outline="black")
            self.toll_points.append((point, zone[0], zone[2]))

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Motion>", self.on_motion)
        self.bind("<Return>", self.confirm_route)

        self.status_label = tk.Label(self, text="Click on toll points to mark your route. Press Enter to confirm.")
        self.status_label.pack()

    def on_click(self, event):
        for point, gps, name in self.toll_points:
            x1, y1, x2, y2 = self.canvas.coords(point)
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                if point not in self.route_points:
                    self.route_points.append(point)
                    self.canvas.itemconfig(point, fill="green")
                    self.status_label.config(text=f"Toll point {name} added to route.")
                else:
                    self.route_points.remove(point)
                    self.canvas.itemconfig(point, fill="blue")
                    self.status_label.config(text=f"Toll point {name} removed from route.")
                break

    def on_motion(self, event):
        for point, gps, name in self.toll_points:
            x1, y1, x2, y2 = self.canvas.coords(point)
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                self.hover_label.place(x=event.x + 10, y=event.y)
                self.hover_label.config(text=name)
                return
        self.hover_label.place_forget()

    def confirm_route(self, event):
        if len(self.route_points) < 2:
            messagebox.showwarning("Insufficient Points", "Please select at least two toll points to calculate the toll.")
            return
        
        route_gps = [gps for point, gps, name in self.toll_points if point in self.route_points]
        
        total_distance = 0.0
        for i in range(len(route_gps) - 1):
            total_distance += geodesic(route_gps[i], route_gps[i+1]).km
        
        toll = self.calculate_toll_cost(total_distance, self.vehicle_type)
        self.status_label.config(text=f"Total Distance: {total_distance:.2f} km. Toll Cost: ₹{toll:.2f}.")

        # Proceed to payment gateway
        self.proceed_to_payment(toll)

    def calculate_toll_cost(self, distance, vehicle_type):
        rates = {
            'Car/Jeep/Van/LMV': 0.65,
            'Light Commercial Vehicle/LGV/Mini-Bus': 1.05,
            'Bus/Truck (2 axles)': 2.20,
            'Three-axle Commercial Vehicle': 2.40,
            'Heavy Construction Machinery/Multi-axle (4-6 axles)': 3.45,
            'Oversized Vehicle (7+ axles)': 4.20
        }
        toll_rate_per_km = rates.get(vehicle_type, 1.0)
        return distance * toll_rate_per_km

    def proceed_to_payment(self, toll):
        response = messagebox.askyesno("Proceed to Payment", f"The toll fare is ₹{toll:.2f}. Do you want to proceed to payment?")
        if response:
            # Simulate payment processing
            messagebox.showinfo("Payment Successful", "Payment has been processed successfully!")
        else:
            messagebox.showinfo("Payment Cancelled", "Payment has been cancelled.")

if __name__ == "__main__":
    vehicle_selection = VehicleSelection()
    vehicle_selection.mainloop()
