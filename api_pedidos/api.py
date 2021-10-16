from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from uuid import UUID
from api_pedidos.excecao import PedidoNaoEncontradoError
from http import HTTPStatus
from api_pedidos.excecao import PedidoNaoEncontradoError, FalhaDeComunicacaoError
from api_pedidos.magalu_api import recuperar_itens_por_pedido
from api_pedidos.esquema import HealthCheckResponse, Item

app = FastAPI()


#def recuperar_itens_por_pedido(identificacao_do_pedido: UUID) -> list[Item]:
#    pass


@app.exception_handler(PedidoNaoEncontradoError)
def tratar_erro_pedido_nao_encontrado(request: Request, exc: PedidoNaoEncontradoError):
    return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"message": "Pedido não encontrado"})


@app.get("/healthcheck", tags=["healthcheck"], summary="Integridade do sistema", description="Checa se o servidor está online")
async def healthcheck():
    return {"status": "ok"}


@app.get("/orders/{identificacao_do_pedido}/items", summary="Itens de um pedido", tags=["pedidos"], description="Retorna todos os itens de um determinado pedido", response_model=list[Item])
def listar_itens(itens: list[Item] = Depends(recuperar_itens_por_pedido)):
    return itens

@app.exception_handler(FalhaDeComunicacaoError)
def tratar_erro_falha_de_comunicacao(request: Request, exc: FalhaDeComunicacaoError):
    return JSONResponse(status_code=HTTPStatus.BAD_GATEWAY, content={"message": "Falha de comunicação com o servidor remoto"})

@app.get("/healthcheck", tags=["healthcheck"], summary="Integridade do sistema", description="Checa se o servidor está online", response_model=HealthCheckResponse)
def healthcheck():
    return HealthCheckResponse(status="ok")