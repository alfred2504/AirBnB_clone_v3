#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  27 09:08:24 2024
Authors: Alfred Makura, Rorisang Moeng
"""

from flask import Blueprint, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity

@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def amenities():
    if request.method == 'GET':
        return jsonify([amenity.to_dict() for amenity in storage.all('Amenity').values()])
    
    elif request.method == 'POST':
        data = request.get_json()
        if not data or not isinstance(data, dict):
            return jsonify({'error': 'Not a JSON'}), 400
        if 'name' not in data:
            return jsonify({'error': 'Missing name'}), 400
        new_amenity = Amenity(**data)
        new_amenity.save()
        return jsonify(new_amenity.to_dict()), 201

@app_views.route('/amenities/<string:amenity_id>', methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def handle_amenity(amenity_id):
    amenity = storage.get('Amenity', amenity_id)
    if not amenity:
        abort(404)
    
    if request.method == 'GET':
        return jsonify(amenity.to_dict())
    
    elif request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    
    elif request.method == 'PUT':
        data = request.get_json()
        if not data or not isinstance(data, dict):
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)
        storage.save()
        return jsonify(amenity.to_dict()), 200
