import uuid
from unittest.mock import MagicMock, patch

import pytest


@pytest.mark.anyio
async def test_get_upload_url(client, test_trip, test_card):
    with patch("app.api.routes.cards.generate_presigned_upload_url") as mock_generate:
        mock_generate.return_value = "https://s3.amazonaws.com/fake-presigned-url"

        response = await client.post(
            f"/trips/{test_trip['id']}/cards/{test_card['id']}/upload-url"
        )

    assert response.status_code == 200
    data = response.json()
    assert "upload_url" in data
    assert "object_key" in data
    assert data["upload_url"] == "https://s3.amazonaws.com/fake-presigned-url"
    assert f"cards/{test_card['id']}" in data["object_key"]


@pytest.mark.anyio
async def test_get_upload_url_card_not_found(client, test_trip):
    with patch("app.api.routes.cards.generate_presigned_upload_url"):
        response = await client.post(
            f"/trips/{test_trip['id']}/cards/{uuid.uuid4()}/upload-url"
        )

    assert response.status_code == 404


@pytest.mark.anyio
async def test_associate_image(client, test_trip, test_card):
    s3_key = f"cards/{test_card['id']}/photo.jpg"
    response = await client.post(
        f"/trips/{test_trip['id']}/cards/{test_card['id']}/images",
        params={"s3_key": s3_key, "is_thumbnail": True, "display_order": 0},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["s3_key"] == s3_key
    assert data["is_thumbnail"] is True
    assert data["display_order"] == 0


@pytest.mark.anyio
async def test_associate_image_card_not_found(client, test_trip):
    response = await client.post(
        f"/trips/{test_trip['id']}/cards/{uuid.uuid4()}/images",
        params={"s3_key": "cards/fake/photo.jpg"},
    )

    assert response.status_code == 404


@pytest.mark.anyio
async def test_generate_presigned_url_unit():
    with patch("app.services.images.boto3.client") as mock_boto_client:
        mock_s3 = MagicMock()
        mock_boto_client.return_value = mock_s3
        mock_s3.generate_presigned_url.return_value = "https://fake-url.com"

        from app.services.images import generate_presigned_upload_url

        url = generate_presigned_upload_url("cards/abc/photo.jpg")

    assert url == "https://fake-url.com"
    mock_s3.generate_presigned_url.assert_called_once_with(
        "put_object",
        Params={"Bucket": unittest_bucket(), "Key": "cards/abc/photo.jpg"},
        ExpiresIn=3600,
    )


def unittest_bucket():
    from app.core.config import settings

    return settings.s3_bucket_name
