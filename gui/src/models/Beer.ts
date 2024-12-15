export enum BeerType {
  PaleLager = "Pale Lager",
  Pilsner = "Pilsner",
  Helles = "Helles",
  Kellerbier = "Kellerbier",
  Zwickelbier = "Zwickelbier",
  Exportbier = "Exportbier",
  ViennaLager = "Vienna Lager",
  AmberLager = "Amber Lager",
  Marzen = "Märzen",
  Dunkel = "Dunkel",
  Schwarzbier = "Schwarzbier",
  Bock = "Bock",
  Doppelbock = "Doppelbock",
  Eisbock = "Eisbock",
  WheatBeer = "Wheat Beer",
  Weissbier = "Weißbier",
  Hefeweizen = "Hefeweizen",
  Kristallweizen = "Kristallweizen",
  Weizenbock = "Weizenbock",
  Ale = "Ale",
  PaleAle = "Pale Ale",
  Sour = "Sour",
  FruitBeer = "Fruit Beer",
  NonAlcoholicBeer = "Non-Alcoholic Beer",
  LowAlcoholBeer = "Low-Alcohol Beer",
  AlcoholFreeWheatBeer = "Alcohol-Free Wheat Beer",
  AlcoholFreeLager = "Alcohol-Free Lager",
}

export interface Beer {
  id: number;
  name: string;
  description: string;
  beer_type: BeerType;
  brewery: string;
  alcohol_content: number;
}