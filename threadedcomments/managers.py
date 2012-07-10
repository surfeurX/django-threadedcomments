#-*- coding: utf-8 -*-
from cache_manager import CacheManager
from django.contrib.contenttypes.models import ContentType
from keys import KEYS 

class ThreadedCommentCacheManager(CacheManager):
    KEYS = KEYS
    
    def comments_for_object(self, query, **kwargs):
        key = self.make_key("comments_for_object", **query)
        queryset = self.get_manager().filter(is_public=True, is_removed=False, **query)
        return self._filter(key, queryset, **kwargs)
    
    def update(self, instance, **kwargs):
        content_type = ContentType.objects.get_for_model(instance.content_object)
        self.comments_for_object(query={"content_type__id":content_type.id,
                                        "object_pk": instance.content_object.id
                                        }, clear=True)
        
class ContentTypeCacheManager(CacheManager):
    KEYS = KEYS 
    
    def get_for_model(self, model, **kwargs):
        opts = self.get_manager()._get_opts(model)
        query = {"app_label": opts.app_label, 
                "model": opts.object_name.lower()}
        key = self.make_key("contenttype_for_object", **query)
        return self._get(key, query=query, **kwargs)
        
ContentType.add_to_class('cache', ContentTypeCacheManager())