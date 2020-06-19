import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
# import models
from models import Tree, Owner, db, setup_db
from auth import AuthError, requires_auth
# import models
import json
import traceback
# from models import Tree, Owner, db
# from flask_migrate import Migrate


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object('config')
    CORS(app)
    setup_db(app)
    # migrate = Migrate(app, db)

    @app.route('/trees')
    def get_trees():
        trees = Tree.query.order_by(Tree.id)    # .all()
        formatted_trees = [tr.format() for tr in trees]

        if len(formatted_trees) == 0:
            abort(404)

        return jsonify({
          'success': True,
          'trees': formatted_trees,
          'total_trees': len(formatted_trees)
        })

    @app.route('/owners')
    @requires_auth('get:owners')
    def get_owners(payload):
        owners = Owner.query.all()  # order_by(Tree.id).all()
        # formatted_categories= [cat.format() for cat in categories]
        formatted_owners = [ob.format() for ob in owners]

        if len(formatted_owners) == 0:
            abort(404)

        return jsonify({
          'success': True,
          'owners': formatted_owners,
          'total_owners': len(owners)
        })

    @app.route('/owners/<owner_id>/trees')
    @requires_auth('get:owners')
    def get_trees_per_owner(payload, owner_id):
        trees = Tree.query.filter_by(owner_id=owner_id).all()

        formatted_trees = [tree.format() for tree in trees]

        if len(formatted_trees) == 0:
            abort(404)

        return jsonify({
          'success': True,
          'trees': formatted_trees,
          'total_trees': len(trees)
        })

    @app.route('/trees', methods=['POST'])
    @requires_auth('post:trees')
    def add_tree(payload):
        print("inside of the add metod", flush=True)
        body = request.get_json()
        print(body, flush=True)

        new_type = body.get('type', None)

        new_owner = body.get('owner_id', None)
        print("new_owner", new_owner, flush=True)

        new_lat = body.get('latitude', None)
        new_long = body.get('longitude', None)

        new_date = body.get('plantedDate', None)
        print("new_date", new_date, flush=True)

        try:
            # tree = Tree(new_type, int(new_owner))
            # print(tree)

            tree = Tree(new_type, int(new_owner),
                        float(new_lat), float(new_long), new_date)
            tree.insert()

            selection = Tree.query.order_by(Tree.id).all()
            formatted_trees = [tr.format() for tr in selection]

            return jsonify({
                'success': True,
                'created': tree.id,
                'trees': formatted_trees,
                'total_trees': len(selection)
                })

        except:
            abort(422)

    @app.route('/trees/<tree_id>', methods=['DELETE'])
    @requires_auth('delete:tree')
    def delete_tree(payload, tree_id):
        try:
            tree = Tree.query.filter(Tree.id == tree_id).one_or_none()

            if tree is None:
                abort(404)

            tree.delete()
            selection = Tree.query.all()
            current_trees = [tr.format() for tr in selection]

            return jsonify({
                  'success': True,
                  'deleted': tree_id,
                  'trees': current_trees,
                  'total_trees': len(current_trees)
              })

        except:
            abort(422)

    @app.route('/trees/<int:id>', methods=['PATCH'])
    @requires_auth('patch:tree')
    def patch_trees(payload, id):
        print("id= " + str(id), flush=True)
        try:
            tree = Tree.query.filter(Tree.id == id).one_or_none()
            print(tree, flush=True)

            if tree is None:
                abort(404)

            body = request.get_json()
            if body is None:
                abort(404)

            new_type = body.get('type', None)
            new_date = body.get('plantedDate', None)

            if new_type is not None:
                tree.type = new_type

            if new_date is not None:
                tree.plantedDate = new_date

            tree.update()

            trees = [x.format() for x in Tree.query.all()]
            return jsonify({
                            "success": True,
                            "trees": trees
                            }), 200
        except:
            (traceback.format_exc()) 
            abort(422)

#    @app.route('/')
#    def index():
#      return redirect(url_for('get_trees_per_owner', owner_id=1))

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
              'success': False,
              'error': 404,
              'message': 'resource not found'
              }), 404

    @app.errorhandler(422)
    def notprocessable(error):
        return jsonify({
              'success': False,
              'error': 422,
              'message': 'unprocessable'
              }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
              'success': False,
              'error': 400,
              'message': 'Bad Request'
              }), 400

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
              'success': False,
              'error': 500,
              'message': 'Internal Server Error'
              }), 500

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
              'success': False,
              'error': 405,
              'message': 'method not allowed'
              }), 405

    @app.errorhandler(AuthError)
    def autherror(error):
        return jsonify({
                      "success": False,
                      "error": error.status_code,
                      "message": error.error
                      }), error.status_code

    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
