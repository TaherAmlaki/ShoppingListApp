from threading import Thread

from flask_login import current_user

from mongoengine.errors import ValidationError

import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

from .models import ShoppingList


class BasketModel:
    def __init__(self):
        self._model = None 
        self._shopping_lists = None
        self.user_id = None
        self._trx_encoder = None
        self._data_df = None
        self._frequent_item_sets = None
        self._item_sets = None
        self._rules = None
        self._process_thread = None

    def set_user_id(self, user_id):
        if self.user_id and self.user_id != user_id:
            self.user_id = user_id
            self.reset()

    def get_rules(self):
        if self._process_thread and self._process_thread.is_alive():
            self._process_thread.join()
            self._process_thread = None
        return self.rules
    
    def get_frequent_item_sets(self):
        if self._process_thread and self._process_thread.is_alive():
            self._process_thread.join()
            self._process_thread = None
        return self.frequent_item_sets

    def reset(self):
        self._shopping_lists = None
        self._trx_encoder = None
        self._data_df = None
        self._frequent_item_sets = None
        self._item_sets = None
        self._rules = None

    @property
    def shopping_lists(self):
        if self.user_id is None:
            self.user_id = current_user.get_id()

        try:    
            if self._shopping_lists is None:
                self._shopping_lists = []
                for lst in ShoppingList.find_by_user_id(self.user_id):
                    self._shopping_lists.append({"name": lst.name, "items": lst.get_items()})
        finally:
            return self._shopping_lists

    @property
    def trx_encoder(self):
        if self._trx_encoder is None:
            self._trx_encoder = TransactionEncoder()
        return self._trx_encoder

    @property
    def data_df(self):
        if self._data_df is None:
            flat_lists = self._pre_process_raw_lists()
            te_ary = self.trx_encoder.fit(flat_lists).transform(flat_lists, sparse=True)
            self._data_df = pd.DataFrame.sparse.from_spmatrix(te_ary, columns=self.trx_encoder.columns_)
        return self._data_df
    
    @property
    def item_sets(self):
        if self._item_sets is None:
            self._item_sets = apriori(self.data_df, min_support=0.1, use_colnames=True)
        return self._item_sets

    @property
    def frequent_item_sets(self):
        if self._frequent_item_sets is None:
            self._frequent_item_sets = [
                {
                    "support": f"{int(100 * round(float(row['support']), 2))}%",
                    "itemsets": ' - '.join([s.title() for s in row['itemsets']])
                }
                for _, row in self.item_sets.iterrows()
            ]
            self._frequent_item_sets.sort(key=lambda itemset_: itemset_["support"], reverse=True)
        return self._frequent_item_sets

    @property
    def rules(self):
        if self._rules is None:
            rules_ = association_rules(self.item_sets, metric="lift", min_threshold=1)
            rules_data = []
            for _, row in rules_.iterrows():
                row = row.T.to_dict()
                d = {
                    "antecedents": " - ".join([s.title() for s in row["antecedents"]]),
                    "consequents": " - ".join([s.title() for s in row["consequents"]]),
                    "confidence": int(100 * round(float(row['confidence']), 2)),
                    "lift": round(row["lift"], 2),
                    "leverage": round(row["leverage"], 2),
                    "conviction": round(row["conviction"], 2)
                }
                rules_data.append(d)
            rules_data.sort(key=lambda r: (-r["lift"], -r["confidence"]))
            self._rules = rules_data
        return self._rules

    def process(self):
        self._process_thread = Thread(target=self._process_thread_target)
        self._process_thread.start()
    
    def _process_thread_target(self):
        return {
            "FrequentItemSets": self.frequent_item_sets,
            "Rules": self.rules
        }

    def _pre_process_raw_lists(self):
        processed_list = [
            [
                item['name'] for item in lst["items"]
            ]
            for lst in self.shopping_lists
        ]
        return processed_list

    @classmethod
    def _to_str_percent(cls, val):
        return f"{int(100 * round(float(val), 2))}%"
