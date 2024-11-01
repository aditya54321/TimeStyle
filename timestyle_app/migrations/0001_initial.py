# Generated by Django 4.2.7 on 2024-05-15 10:59

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_manufactured', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered')], default='Pending', max_length=20)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('in_cart', models.BooleanField(default=False)),
                ('quantity', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(blank=True, max_length=150)),
                ('last_name', models.CharField(blank=True, max_length=150)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('mobile_number', models.CharField(blank=True, max_length=15, null=True)),
                ('password', models.CharField(max_length=100)),
                ('registration_date', models.DateField(auto_now_add=True)),
                ('last_login', models.DateField(default=django.utils.timezone.now)),
                ('is_administrator', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('email_verified', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'custome user',
                'verbose_name_plural': 'custome users',
            },
        ),
        migrations.CreateModel(
            name='WatchDesign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='watch_designs/')),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('razorpay_id', models.CharField(blank=True, max_length=100, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Failed', 'Failed'), ('Successful', 'Successful')], default='Pending', max_length=20)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timestyle_app.cart')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timestyle_app.users')),
            ],
        ),
        migrations.CreateModel(
            name='OrderReceipt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_quantity', models.PositiveIntegerField(default=1)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timestyle_app.cart')),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timestyle_app.payment')),
            ],
        ),
        migrations.CreateModel(
            name='DesignDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('watch_face', models.CharField(max_length=100)),
                ('strap', models.CharField(max_length=100)),
                ('dial', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('movement', models.CharField(max_length=100, null=True)),
                ('features', models.TextField(default='Water Resistant')),
                ('watch_design', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='timestyle_app.watchdesign')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='design',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timestyle_app.designdetails'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timestyle_app.users'),
        ),
    ]