from flask import Flask, Response
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from common.extensions import db,api,docs
from resources.book_resources import BookResource,BookListResource
from resources.user_resources import UserResource

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:Cnm233@127.0.0.1/testdb'

    app.config.update({
        'APISPEC_SPEC': APISpec(
            title='Restful API proj',
            version='v1',
            plugins=[MarshmallowPlugin()],
            openapi_version='2.0.0'
        ),
        'APISPEC_SWAGGER_URL': '/swagger/',
        'APISPEC_SWAGGER_UI_URL': '/swagger-ui/',
    })

    db.init_app(app)
    docs.init_app(app)

    '''             原方案中（上一版本），将注册分散在各resources中
                    结构优化后，原来用的 MethodResource + Flask-Restful的Api.add_resource注册路由
                    但在flask-apispec中不会自动生效，需要额外处理
                    查询后原因：MethodResource 是为 flask_apispec 文档注册设计的，但
                    它并不会自动绑定到 Api 实例上的 Flask 路由中。
                    而 Api.add_resource(...) 只对纯 Resource 生效
                    
    api.add_resource(BookResource, '/books/<int:book_id>', endpoint='bookResource')
    api.add_resource(BookListResource, '/books', endpoint='bookListResource')
    api.add_resource(LoginResource, '/login', endpoint='loginResource')
    '''

    #改为使用Flask原生 add_url_rule 注册 MethodResource路由

    app.add_url_rule(
        '/books/<int:book_id>',
        view_func=BookResource.as_view('bookResource'),
        methods=['GET', 'PUT', 'DELETE']
    )

    app.add_url_rule(
        '/books',
        view_func=BookListResource.as_view('bookListResource'),
        methods=['GET', 'POST']
    )

    app.add_url_rule(
        '/user',
        view_func=UserResource.as_view('userResource'),
        methods=['POST']
    )

    docs.register(BookResource, endpoint='bookResource')
    docs.register(BookListResource, endpoint='bookListResource')
    docs.register(UserResource, endpoint='userResource')

    @app.route('/swagger.yaml')
    def generate_swagger_yaml():
        yaml_doc = docs.spec.to_yaml()
        return Response(yaml_doc, mimetype='text/x-yaml')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)