import unittest
import json
import requests_mock

import gazu.asset
import gazu.client

from utils import fakeid


class AssetTestCase(unittest.TestCase):
    def test_all_entities(self):
        entities = [
            {"id": "asset-01", "name": "Asset 01", "project_id": "project-01"},
            {"id": "shot-01", "name": "Shot 01", "project_id": "project-01"},
        ]
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url("data/entities"),
                text=json.dumps(entities),
            )

            self.assertEqual(gazu.entity.all_entities(), entities)

    def test_get_entity(self):
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url("data/entities/asset-01"),
                text=json.dumps(
                    {
                        "id": "asset-01",
                        "name": "Asset 01",
                        "project_id": "project-01",
                    }
                ),
            )
            entity = gazu.entity.get_entity("asset-01")
            self.assertEqual(entity["name"], "Asset 01")
            self.assertEqual(entity["project_id"], "project-01")

    def test_get_entity_type(self):
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url("data/entity-types/characters"),
                text=json.dumps({"id": "characters", "name": "Characters"}),
            )
            entity = gazu.entity.get_entity_type("characters")
            self.assertEqual(entity["name"], "Characters")

    def test_new_entity_type(self):
        entity_type_name = "Characters"
        with requests_mock.mock() as mock:
            entity_type = {"id": "entity-type-1", "name": entity_type_name}
            mock.post(
                gazu.client.get_full_url("data/entity-types"),
                text=json.dumps(entity_type),
            )
            self.assertEqual(
                gazu.entity.new_entity_type(entity_type_name), entity_type
            )

    def test_all_entity_types(self):
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url("data/entity-types"),
                text=json.dumps(
                    [
                        {
                            "id": fakeid("entity-type-1"),
                            "name": "entity-type-1",
                        },
                        {
                            "id": fakeid("entity-type-2"),
                            "name": "entity-type-2",
                        },
                    ]
                ),
            )
            entity_types = gazu.entity.all_entity_types()
            self.assertEqual(len(entity_types), 2)
            self.assertEqual(entity_types[0]["id"], fakeid("entity-type-1"))
            self.assertEqual(entity_types[1]["id"], fakeid("entity-type-2"))

    def test_get_entity_by_name(self):
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url("data/entities?name=entity-1"),
                text=json.dumps(
                    [{"id": fakeid("entity-1"), "name": "entity-1"}]
                ),
            )
            entity = gazu.entity.get_entity_by_name("entity-1")
            self.assertEqual(entity["id"], fakeid("entity-1"))

    def test_get_entity_type_by_name(self):
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url(
                    "data/entity-types?name=entity-type-1"
                ),
                text=json.dumps(
                    [{"id": fakeid("entity-type-1"), "name": "entity-type-1"}]
                ),
            )
            entity_type = gazu.entity.get_entity_type_by_name("entity-type-1")
            self.assertEqual(entity_type["id"], fakeid("entity-type-1"))
