from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import Sum

class Product(models.Model):
	product_name = models.CharField(max_length=150)
	product_type = models.CharField(max_length=25)
	product_description = models.TextField()
	affiliate_url = models.SlugField(blank=True, null=True)
	product_image = models.ImageField(upload_to='images/')
	pricing_average = models.DecimalField(default=0, max_digits=3, decimal_places=1)
	performance_average = models.DecimalField(default=0, max_digits=3, decimal_places=1)
	durability_average = models.DecimalField(default=0, max_digits=3, decimal_places=1)
	is_available = models.BooleanField(default=True)
	stock = models.PositiveIntegerField(default=0)

	def update_availability(self):
		"""Update the product's availability based on stock count."""
		if self.stock == 0:
			self.is_available = False
		else:
			self.is_available = True
		self.save()

	def save(self, *args, **kwargs):
		"""Override the save method to update availability."""
		if self.stock == 0:
			self.is_available = False
		else:
			self.is_available = True

		super(Product, self).save(*args, **kwargs)  # Call the "real" save method

	def __str__(self):
		return self.product_name

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	products = models.ManyToManyField(Product)

	@receiver(post_save, sender=User)
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			Profile.objects.create(user=instance)

	@receiver(post_save, sender=User)
	def save_user_profile(sender, instance, **kwargs):
		instance.profile.save()

class Vote(models.Model):   #add this class and the following fields
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	pricing = models.IntegerField(default=0)
	performance = models.IntegerField(default=0)
	durability = models.IntegerField(default=0)

	def calculate_averages(self):
			product = self.product
			vote_qs = Vote.objects.filter(product=product)
			vote_count = vote_qs.count()
			pricing_total = vote_qs.aggregate(Sum('pricing'))
			performance_total = vote_qs.aggregate(Sum('performance'))
			durability_total = vote_qs.aggregate(Sum('durability'))
			product.pricing_average = pricing_total['pricing__sum']/vote_count
			product.performance_average = performance_total['performance__sum']/vote_count
			product.durability_average = durability_total['durability__sum']/vote_count
			product.save()

