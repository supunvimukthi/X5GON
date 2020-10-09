from x5gon_rest.fieldnames import VALUE
from x5gon_rest.x5db_app import app


def test_language_post():
    resp = app.test_client().post("language_detection", json={
        VALUE: "SLAVKO OSTERC (1895–1941)\nSlavko Osterc\nse je rodil v Veržeju pri Ljutomeru. Poleg Marija Kogoja je "
               "začetnik slovenske\nsodobne glasbe. Pomembna prelomnica na njegovi glasbeni poti je njegov odhod v "
               "Prago.\nTam je študiral kompozicijo, dirigiranje in operno režijo. Po vrnitvi v\nLjubljano, "
               "leta 1927, je do svoje smrti poučeval na Konservatoriju in Akademiji\nza glasbo.\nSlavko Osterc je v "
               "slovensko glasbo prinesel svežino, ki ni več dopuščala\npretirane čustvenosti. Izražal se je s "
               "sredstvi, značilnimi za evropski\nneoklasicizem. Zaradi svojega pristopa je po drugi svetovni vojni "
               "postal\nvzornik mlajšim skladateljem.\nSuita za orkester (1929), ki jo je skladatelj napisal po "}
                                  )

    assert resp.status_code == 200

    resp_dict = resp.get_json()

    assert type(resp_dict) == dict
