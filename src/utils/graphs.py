import matplotlib.pyplot as plt
import asyncio
import uuid

def _create_plot(data):
    random_name = f'data_img_{uuid.uuid4()}.png'

    plt.figure(figsize=(10, 6))
    plt.bar(data.group_name, data.mat_counter)
    plt.xlabel('Группы')
    plt.ylabel('Кол-во нарушений')
    plt.title('Топ нарушителей')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(random_name)
    plt.close()
    return random_name

async def generate_stats_graph(data):
    loop = asyncio.get_running_loop()
    filename = await loop.run_in_executor(None, _create_plot, data)
    return filename