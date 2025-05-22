import click
from flask.cli import with_appcontext
from app.utils.db_seeder import seed_database
from app.utils.realtime_simulator import start_simulator, stop_simulator

@click.command('seed-db')
@click.option('--customers', default=50, help='Number of customers to seed')
@click.option('--devices', default=100, help='Number of devices to seed')
@click.option('--days', default=7, help='Days of health data history')
@click.option('--feedback', default=20, help='Number of feedback entries')
@with_appcontext
def seed_db_command(customers, devices, days, feedback):
    """初始化数据库，生成模拟数据"""
    click.echo('开始初始化数据库...')
    result = seed_database(customers, devices, days, feedback)
    click.echo(f"数据库初始化完成！")
    click.echo(f"创建了 {result['customers']} 个客户，{result['devices']} 个设备")
    click.echo(f"每个设备生成了 {result['days_of_health_data']} 天的健康数据")
    click.echo(f"创建了 {result['feedback_entries']} 条用户反馈")

@click.command('start-simulator')
@with_appcontext
def start_simulator_command():
    """启动实时数据模拟器"""
    click.echo('正在启动实时数据模拟器...')
    success = start_simulator()
    if success:
        click.echo('实时数据模拟器已启动')
    else:
        click.echo('实时数据模拟器启动失败，可能已经在运行')

@click.command('stop-simulator')
@with_appcontext
def stop_simulator_command():
    """停止实时数据模拟器"""
    click.echo('正在停止实时数据模拟器...')
    success = stop_simulator()
    if success:
        click.echo('实时数据模拟器已停止')
    else:
        click.echo('实时数据模拟器停止失败，可能已经停止运行')

def register_cli_commands(app):
    """Register CLI commands with the app"""
    app.cli.add_command(seed_db_command)
    app.cli.add_command(start_simulator_command)
    app.cli.add_command(stop_simulator_command) 