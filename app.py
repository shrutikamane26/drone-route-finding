from flask import Flask, request, jsonify
import heapq

app = Flask(__name__)

class Graph:
    def __init__(self):
        self.edges = {}
    
    def add_edge(self, node1, node2, distance):
        if node1 not in self.edges:
            self.edges[node1] = {}
        if node2 not in self.edges:
            self.edges[node2] = {}
        
        self.edges[node1][node2] = distance
        self.edges[node2][node1] = distance

def heuristic(node, goal):
    return 0

def a_star(graph, start, goal):
    open_list = [(0, start)]
    came_from = {}
    g_score = {node: float('inf') for node in graph.edges}
    g_score[start] = 0
    f_score = {node: float('inf') for node in graph.edges}
    f_score[start] = heuristic(start, goal)
    
    while open_list:
        current_f_score, current_node = heapq.heappop(open_list)
        
        if current_node == goal:
            path = []
            while current_node in came_from:
                path.append(current_node)
                current_node = came_from[current_node]
            path.append(start)
            return path[::-1]
        
        for neighbor, distance in graph.edges[current_node].items():
            tentative_g_score = g_score[current_node] + distance
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current_node
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
                heapq.heappush(open_list, (f_score[neighbor], neighbor))
    
    return None

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Drone Delivery System</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
            }

            .container {
                max-width: 600px;
                margin: 50px auto;
                padding: 20px;
                background-color: #fff;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }

            .form-group {
                margin-bottom: 15px;
            }

            label {
                display: block;
                margin-bottom: 5px;
            }

            select {
                width: 100%;
                padding: 10px;
                border-radius: 4px;
                border: 1px solid #ccc;
            }

            button {
                padding: 10px 20px;
                background-color: #007BFF;
                color: #fff;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }

            button:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Drone Delivery System</h1>
            
            <div class="form-group">
                <label for="start">Start Node:</label>
                <select id="start">
                    <option value="A">A</option>
                    <option value="B">B</option>
                    <option value="C">C</option>
                    <option value="D">D</option>
                    <option value="E">E</option>
                    <option value="F">F</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="destination">Destination Node:</label>
                <select id="destination">
                    <option value="A">A</option>
                    <option value="B">B</option>
                    <option value="C">C</option>
                    <option value="D">D</option>
                    <option value="E">E</option>
                    <option value="F">F</option>
                </select>
            </div>
            
            <button onclick="getRoute()">Get Route</button>
            
            <div id="weather-conditions"></div>
            <div id="route-recommendations"></div>

            <script>
                function getRoute() {
                    const start = document.getElementById('start').value;
                    const destination = document.getElementById('destination').value;

                    const data = {
                        start,
                        destination
                    };

                    fetch('/get_route', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(data),
                    })
                    .then(response => response.json())
                    .then(data => {
                        displayWeatherConditions(data.weather_conditions);
                        displayRouteRecommendations(data.route_recommendations.route);
                    })
                    .catch((error) => {
                        console.error('Error:', error);
                    });
                }

                function displayWeatherConditions(conditions) {
                    const weatherDiv = document.getElementById('weather-conditions');
                    weatherDiv.innerHTML = `<h3>Weather Conditions</h3>
                                            <p>Start: ${conditions.start}</p>
                                            <p>Midpoint: ${conditions.midpoint}</p>
                                            <p>Destination: ${conditions.destination}</p>`;
                }

                function displayRouteRecommendations(route) {
                    const routeDiv = document.getElementById('route-recommendations');
                    let html = `<h3>Route Recommendations</h3>`;
                    route.forEach(step => {
                        html += `<p>${step.location}: ${step.action}</p>`;
                    });
                    routeDiv.innerHTML = html;
                }
            </script>
        </div>
    </body>
    </html>
    '''

@app.route('/get_route', methods=['POST'])
def get_route():
    graph = Graph()
    graph.add_edge("A", "B", 5)
    graph.add_edge("A", "C", 7)
    graph.add_edge("B", "C", 3)
    graph.add_edge("B", "D", 9)
    graph.add_edge("C", "D", 2)
    graph.add_edge("C", "E", 8)
    graph.add_edge("D", "F", 4)
    graph.add_edge("E", "F", 6)
    
    data = request.json
    start = data.get('start')
    goal = data.get('destination')
    
    path = a_star(graph, start, goal)
    
    # Dummy weather conditions
    weather_conditions = {
        'start': 'Sunny',
        'midpoint': 'Cloudy',
        'destination': 'Rainy'
    }
    
    # Generate route recommendations
    route_recommendations = {
        'route': [
            {'location': node, 'action': 'Fly to next node'} for node in path
        ]
    }
    
    return jsonify({
        'weather_conditions': weather_conditions,
        'route_recommendations': route_recommendations
    })

if __name__ == '__main__':
    app.run(debug=True)
