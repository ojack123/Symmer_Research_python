from t_rrt_time_varied import *
from json_converter import *

path_file = "four_wait_wait_example.txt"

def main():
    json_data = JsonData('saved_paths/' + path_file)
    way, head, thort, path = json_data.get_path_information()

    # with open('saved_paths/' + path_file) as json_file:
    #     data = json.load(json_file)
    #     cost_map = np.array(data['cost'])
    #     mesh_grid = np.array([data['mesh_grid'][0], data['mesh_grid'][1]])
    #     path = []
    #     for i in range(0, len(data['t'])):
    #         point = [data['path']['waypoints'][i][0], data['path']['waypoints'][i][1],
    #                  data['t'][i], data['path']['heading'][i], data['path']['throttle'][i]]
    #         path.append(point)

    plt.figure(1)
    plt.subplot(211)
    plt.plot([t for (x, y, t, psi, throttle) in path], [throttle for (x, y, t, psi, throttle) in path])
    plt.ylabel("acceleration (m/s^2)")

    plt.subplot(212)
    plt.plot([t for (x, y, t, psi, throttle) in path], [(180 / np.pi) * psi for (x, y, t, psi, throttle) in path])
    plt.xlabel("time (sec)")
    plt.ylabel("heading (deg)")

    while True:
        for t_idx in range(0, len(json_data.data['t'])):
            plt.figure(2)
            plt.clf()
            plt.ion()
            plt.contourf(json_data.mesh_grid[0], json_data.mesh_grid[1], json_data.cost_map[t_idx], 20, cmap='inferno')
            plt.plot([x for (x, y, t, psi, throttle) in path[:t_idx]], [y for (x, y, t, psi, throttle) in path[:t_idx]], '-r')
            plt.grid(True)
            plt.xlabel('x (meters)')
            plt.ylabel('y (meters)')
            plt.title(path_file)
            plt.show()
            plt.pause(0.5)





if __name__ == '__main__':
    main()
