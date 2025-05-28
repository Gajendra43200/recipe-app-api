[1mdiff --git a/app/recipe/tests/test_tags_api.py b/app/recipe/tests/test_tags_api.py[m
[1mindex f93e8f8..fb29652 100644[m
[1m--- a/app/recipe/tests/test_tags_api.py[m
[1m+++ b/app/recipe/tests/test_tags_api.py[m
[36m@@ -12,6 +12,11 @@[m [mfrom recipe.serializers import ([m
 [m
 TAG_URL = reverse('recipe:tag-list')[m
 [m
[32m+[m[32mdef detail_url(tag_id):[m
[32m+[m[32m    # Create and return a tag detail_url[m
[32m+[m[32m    return reverse('recipe:tag-detail', args=[tag_id])[m
[32m+[m
[32m+[m
 def create_user(email='user@example.com', password='testpass123'):[m
     return get_user_model().objects.create_user(email=email, password=password)[m
 [m
[36m@@ -58,5 +63,26 @@[m [mclass PrivateTagsApiTests(TestCase):[m
         self.assertEqual(len(res.data), 1)[m
         self.assertEqual(res.data[0]['name'], tag.name)[m
         self.assertEqual(res.data[0]['id'], tag.id)[m
[32m+[m
[32m+[m[32m    def test_update_tag(self):[m
[32m+[m[32m        # Test updating tag[m[41m [m
[32m+[m[32m        tag = Tag.objects.create(user=self.user, name='After dinner')[m
[32m+[m[32m        payload = {'name': 'Dessert'}[m
[32m+[m[32m        url = detail_url(tag.id)[m
[32m+[m[32m        res = self.client.patch(url, payload)[m
[32m+[m[32m        self.assertEqual(res.status_code, status.HTTP_200_OK)[m
[32m+[m[32m        tag.refresh_from_db()[m
[32m+[m[32m        self.assertEqual(tag.name, payload['name'])[m
[32m+[m[41m    [m
[32m+[m[32m    def test_delete_tag(self):[m
[32m+[m[32m        # Test deleting a tag.[m
[32m+[m[32m        tag = Tag.objects.create(user=self.user, name='Breakfast')[m
[32m+[m[32m        url = detail_url(tag.id)[m
[32m+[m[32m        res = self.client.delete(url)[m
[32m+[m
[32m+[m[32m        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)[m
[32m+[m[32m        tags =  Tag.objects.filter(user=self.user)[m
[32m+[m[32m        self.assertFalse(tags.exists())[m
[41m+[m
         [m
 [m
