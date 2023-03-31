from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request

from core.config import CommonQueryParams
from models.film import Person, PersonList
from services.persons import PersonService, get_person_service

router = APIRouter()


@router.get(
    "",
    response_model=list[PersonList],
    description="Полнотекстовый поиск по персонам с пагинацией",
    summary="Полнотекстовый поиск по персонам",
    response_description="Список персон",
)
async def list_persons(
    person_service: PersonService = Depends(get_person_service),
    commons: CommonQueryParams = Depends(CommonQueryParams),
) -> list[PersonList]:
    persons = await person_service.get_data_list(
        page_number=commons.page_number, page_size=commons.page_size
    )
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return [
        PersonList(
            id=person["id"],
            full_name=person["full_name"],
        )
        for person in persons
    ]


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
    persons = await person_service.search_data(query, commons.page_number, commons.page_size)
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return [
        Person(
            id=person["id"],
            full_name=person["full_name"],
            films=person["films"],
        )
        for person in persons
    ]


@router.get(
    "/{person_id}",
    response_model=Person,
    summary="Получение одной персоны",
    description="Получить информацию о персоне",
    response_description="Подробная информация о персоне",
)
async def person_details(
    request: Request, person_id: UUID, person_service: PersonService = Depends(get_person_service)
) -> Person:
    person = await person_service.get_data_by_id(url=str(request.url), id=str(person_id))
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return Person(
        id=person["id"],
        full_name=person["full_name"],
        films=person["films"],
    )
