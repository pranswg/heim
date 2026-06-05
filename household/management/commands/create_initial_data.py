import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from household.models import InventoryItem, Expense, RequestItem
from faker import Faker

class Command(BaseCommand):
    help = 'Populates the household tracking platform with sample evaluation data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        # 1. Seed Core Family Users
        self.stdout.write("Generating sample household users...")
        family_members = ['Alice', 'Bob', 'Charlie', 'Diana']
        users = []
        for name in family_members:
            user, created = User.objects.get_or_create(
                username=name.lower(),
                defaults={'first_name': name, 'email': f'{name.lower()}@household.local'}
            )
            if created:
                user.set_password('housepass123')
                user.save()
            users.append(user)

        # 2. Seed Common Inventory Supplies
        self.stdout.write("Generating grocery and supply inventory...")
        sample_items = [
            ('Eggs', 'pieces'), ('Milk', 'liters'), ('Bread', 'loaves'),
            ('Rice', 'kg'), ('Paracetamol', 'tablets'), ('Dish Soap', 'bottles')
        ]
        for item_name, unit in sample_items:
            InventoryItem.objects.create(
                item_name=item_name,
                current_stock=random.randint(0, 15),
                min_stock_threshold=random.randint(2, 5),
                unit=unit
            )

        # 3. Seed Realistic Expense Logs
        self.stdout.write("Generating localized out-of-pocket transactions...")
        categories = ['Groceries', 'Medical', 'Utilities', 'Personal Care', 'Entertainment']
        expenses = []
        for _ in range(15):
            expense = Expense.objects.create(
                buyer=random.choice(users),
                amount=round(random.uniform(5.50, 150.00), 2),
                category=random.choice(categories),
                description=fake.sentence(nb_words=6)
            )
            expenses.append(expense)

        # 4. Seed Dynamic Request Queues
        self.stdout.write("Generating personal request logs...")
        urgencies = ['Low', 'Medium', 'High']
        statuses = ['Pending', 'Fulfilled', 'Cancelled']
        request_items = ['Cough Syrup', 'Batteries', 'Toilet Paper', 'Coffee Beans', 'Vitamin C']
        
        for item in request_items:
            status = random.choice(statuses)
            # If fulfilled, link it optionally to an existing transaction record
            linked_expense = random.choice(expenses) if status == 'Fulfilled' else None
            
            RequestItem.objects.create(
                requester=random.choice(users),
                item_name=item,
                specification=fake.word() + " pack" if random.choice([True, False]) else None,
                quantity=f"{random.randint(1, 4)} packs",
                urgency=random.choice(urgencies),
                status=status,
                associated_expense=linked_expense
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded full tracking data arrays!'))