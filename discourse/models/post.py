from .jsonobject import JSONObject


class Post(JSONObject):
    def update(self, raw=None, raw_old=None, edit_reason=None, cooked=None):
        params = {
            "post[raw]": raw,
            "post[raw_old]": raw_old,
            "post[edit_reason]": edit_reason,
            "post[cooked]": cooked,
        }
        return self.session.request(
            "PUT", "posts/{}.json".format(self.id), params=params
        )

    def lock(self, locked):
        params = {"locked": locked}
        response = self.session.request(
            "PUT", "posts/{}/locked".format(self.id), params=params
        )

        return response

    def action(self, action):
        # Must understand what the action fields represent before implementing
        # return Post(), True or False
        # "actions_summary": [
        #     {
        #         "can_act": true,
        #         "id": 2
        #     },
        #     {
        #         "can_act": true,
        #         "id": 3
        #     },
        #     {
        #         "can_act": true,
        #         "id": 4
        #     },
        #     {
        #         "can_act": true,
        #         "id": 8
        #     },
        #     {
        #         "can_act": true,
        #         "id": 7
        #     }
        # ],
        raise NotImplementedError
