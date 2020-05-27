from django.db import models


class users(models.Model):
    user_name = models.CharField(max_length=100)

    def __str__(self):
        return self.user_name

# class username_used(models.Model):
#     i_id = models.ForeignKey(users, on_delete=models.CASCADE)
#     insta_ids = models.CharField(max_length=100)


class ids(models.Model):
    i_id = models.ForeignKey(users, on_delete=models.CASCADE)
    id_user = models.CharField(max_length=100)

    def __str__(self):
        return self.id_user


class ids_con(models.Model):
    id_cons = models.CharField(max_length=100)

    def __str__(self):
        return self.id_cons