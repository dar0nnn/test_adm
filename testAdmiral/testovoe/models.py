from django.db import models


class Category(models.Model):
    """
    Модель похожая на список смежных вершин (Adjacency list)
    """
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        db_index=True,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=50)

    def get_descendants(self, include_self=False):
        """
        ищет потомков
        """
        sql = """WITH RECURSIVE t AS (
          SELECT * FROM testovoe_category WHERE id = %s
          UNION
          SELECT testovoe_category.* FROM testovoe_category JOIN t ON testovoe_category.parent_id = t.id
        )
        SELECT * FROM t"""

        if not include_self:
            sql += " OFFSET 1"

        return Category.objects.raw(sql, [self.id])