import matplotlib
matplotlib.use('TkAgg')  # явно указать backend для стабильности
import matplotlib.pyplot as plt

epochs = []
scores = []

plt.ion()
fig, ax = plt.subplots()
(line,) = ax.plot([], [], color='orange', linewidth=1)
sc = ax.scatter([], [], c='blue', s=10)
ax.set_xlabel('Epoch')
ax.set_ylabel('Score')
ax.set_title('Snake AI Training Progress')
plt.show(block=False)  # не блокировать основной поток

def update_stats(epoch, score):
    epochs.append(epoch)
    scores.append(score)
    # Обновить данные линии и точек без очистки оси
    line.set_data(epochs, scores)
    sc.set_offsets(list(zip(epochs, scores)))  # обновить точки без пересоздания scatter
    ax.relim()
    ax.autoscale_view()
    ax.set_xlabel('Epoch')
    ax.set_ylabel('Score')
    ax.set_title('Snake AI Training Progress')
    fig.canvas.flush_events()  # обработка событий окна
    plt.pause(0.001)
    plt.pause(0.001)
