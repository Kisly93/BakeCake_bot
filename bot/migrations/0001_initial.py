# Generated by Django 4.2 on 2023-07-29 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cake',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.IntegerField()),
                ('image', models.ImageField(upload_to='cakes/')),
            ],
        ),
        migrations.CreateModel(
            name='CakeConstructor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_of_level', models.CharField(choices=[('one', '1 уровень'), ('two', '2 уровня'), ('three', '3 уровня')], default='one', max_length=5, verbose_name='Количество уровней торта')),
                ('cake_shape', models.CharField(choices=[('square', 'Квадрат'), ('circle', 'Круг'), ('rectangle', 'Прямоугольник')], default='circle', max_length=20, verbose_name='Форма торта')),
                ('base_of_cake', models.CharField(choices=[('vanila', 'Ванильный бисквит'), ('choco', 'Шоколадный бисквит'), ('marble', 'Мраморный бисквит'), ('honey_biscuits', 'Медовое печенье')], default='vanila', max_length=20, verbose_name='Основа для торта')),
                ('topping', models.CharField(blank=True, choices=[('wedge', 'Кленовый сироп'), ('caramel', 'Карамельный сироп'), ('milk_choco', 'Молочный шоколад'), ('blueberry_syrup', 'Черничный сироп'), ('strawberry_syrup', 'Клубничный сироп'), ('white_sauce', 'Белый соус')], max_length=20, verbose_name='Топпинг')),
                ('berries', models.CharField(blank=True, choices=[('blackberry', 'Еживика'), ('raspberry', 'Малина'), ('blueberry', 'Голубика'), ('strawberry', 'Клубника')], max_length=20, verbose_name='Ягоды')),
                ('inscription', models.CharField(blank=True, max_length=200, verbose_name='Надпись на торте')),
                ('price', models.IntegerField(verbose_name='Цена')),
            ],
        ),
        migrations.CreateModel(
            name='LinkStatistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=200, verbose_name='Простая ссылка')),
                ('bitlink', models.CharField(blank=True, max_length=200, verbose_name='Bitly ссылка')),
                ('description', models.TextField(verbose_name='Описание ссылки')),
                ('transitions', models.IntegerField(default=0, verbose_name='Количество переходов по ссылке')),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='ID чата участника')),
                ('name', models.CharField(blank=True, max_length=40, null=True, verbose_name='Имя участника')),
            ],
        ),
        migrations.CreateModel(
            name='CakeOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=100, null=True)),
                ('user_name', models.CharField(max_length=100, null=True)),
                ('user_phone', models.CharField(max_length=20, null=True)),
                ('delivery_date', models.DateField(null=True)),
                ('delivery_time', models.TimeField(null=True)),
                ('delivery_address', models.CharField(max_length=200, null=True)),
                ('cake', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bot.cake')),
            ],
        ),
    ]
