from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request

from models.film import Person, PersonList
from services.persons import PersonService, get_person_service

router = APIRouter()


@router.get(
    "/{person_id}",
    response_model=Person,
    summary="Персона",
    description="Получить информацию о персоне",
    response_description="Подробная информация о персоне",
)
async def person_details(
    request: Request, person_id: str, person_service: PersonService = Depends(get_person_service)
) -> Person:
    query_params = dict(person_id=person_id, request=request, index="persons")
    person = await person_service.get_data_by_id(query_params)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return Person(
        id=person.id,
        full_name=person.full_name,
        films=person.films,
    )


@router.get(
    "/",
    response_model=list[PersonList],
    description="Список персон",
    summary="Список персон",
    response_description="Список персон",
)
async def list_persons(
    request: Request,
    person_service: PersonService = Depends(get_person_service),
    page_number=1,
    page_size=20,
) -> list[PersonList]:
    query_params = dict(
        request=request,
        index="persons",
        page_number=page_number,
        page_size=page_size,
    )
    persons = await person_service.get_data_list(query_params)
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return [PersonList(id=person.id, full_name=person.full_name) for person in persons]
