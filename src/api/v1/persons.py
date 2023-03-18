from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query, Request

from models.film import Person, PersonList
from services.persons import PersonService, get_person_service

router = APIRouter()


class CommonQueryParams:
    def __init__(
        self,
        page_number: int | None = Query(default=1, ge=1),
        page_size: int | None = Query(default=10, ge=1, le=50),
    ):
        self.page_number = page_number
        self.page_size = page_size


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
    commons: CommonQueryParams = Depends(CommonQueryParams),
) -> list[PersonList]:
    query_params = dict(
        request=request,
        index="persons",
        page_number=commons.page_number,
        page_size=commons.page_size,
    )
    persons = await person_service.get_data_list(query_params)
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return [PersonList(id=person.id, full_name=person.full_name) for person in persons]


@router.get(
    "/search",
    response_model=list[Person],
    description="Список персон",
    summary="Список персон",
    response_description="Список персон",
)
async def search_persons(
    query: str = "",
    person_service: PersonService = Depends(get_person_service),
    commons: CommonQueryParams = Depends(CommonQueryParams),
) -> list[Person]:
    persons = await person_service.search_persons(query, commons.page_number, commons.page_size)
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return [
        Person(
            id=person["_source"]["id"],
            full_name=person["_source"]["full_name"],
            films=person["_source"]["films"],
        )
        for person in persons
    ]


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
