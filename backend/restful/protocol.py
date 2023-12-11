from flask import Blueprint, request, Markup, make_response
import flask_restx
import context
import markdown
import flask


protocol_blueprint = Blueprint("Protocol-API", __name__)
api = flask_restx.Api(protocol_blueprint)


class UserAgreement(flask_restx.Resource):
    def get(self):
        if len(context.config["user_agreement_file"]) > 0:
            filename = context.config["user_agreement_file"]
            with open(filename) as fin:
                content = fin.read()
                pass

            content = Markup(markdown.markdown(content))
            return make_response(content)
            pass
        pass


class PrivacyPolicy(flask_restx.Resource):
    def get(self):
        if len(context.config["privacy_policy_file"]) > 0:
            filename = context.config["privacy_policy_file"]
            with open(filename) as fin:
                content = fin.read()
                pass

            content = Markup(markdown.markdown(content))
            return make_response(content)
            pass
        pass


api.add_resource(UserAgreement, "/user_agreement")
api.add_resource(PrivacyPolicy, "/privacy_policy")
