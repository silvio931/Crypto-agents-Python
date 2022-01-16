#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import spade
from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour
import random

cijenaKriptovalute = 0
kolicinaKupnje = ""
kolicinaZaProdaju = "0"
iznosKupnja = ""
iznosProdaja = ""
ukupanIznosKupnje = 0
ukupanIznosProdaje = 0

class Okruzje(Agent):
    class PosaljiPoruku(PeriodicBehaviour):
        async def run(self):
            global cijenaKriptovalute
            generiranjaCijenaDonja = cijenaKriptovalute-cijenaKriptovalute*0.1
            generiranaCijenaGornja = cijenaKriptovalute+cijenaKriptovalute*0.1
            cijenaKriptovalute = random.randint(int(generiranjaCijenaDonja), int(generiranaCijenaGornja))
            msg = spade.message.Message(
                to="smihalic_1@rec.foi.hr",
                body=str(cijenaKriptovalute),
                metadata={
                    "language": "hrvatski",
                    "performative": "inform"})
            await self.send(msg)
            
    async def setup(self):
        await signalAgent.start()
        await kupiAgent.start()
        await prodajAgent.start()

        print("Okruzje se pokrece!")
        
        start_at=datetime.datetime.now()
        posalji=self.PosaljiPoruku(period=5, start_at = start_at)
        self.add_behaviour(posalji)

class SignalAgent(Agent):
    class AnalizirajCijenu(PeriodicBehaviour):
        async def run(self):
            msg = await self.receive()
            if msg:
                print(msg.body)
                if(int(iznosKupnja) >= int(msg.body) and int(kolicinaKupnje) > 0):
                    msg2 = spade.message.Message(
                        to="smihalic_3@rec.foi.hr",
                        body=msg.body,
                        metadata={
                            "language": "hrvatski",
                            "performative": "inform"})
                    await self.send(msg2)
                if(int(iznosProdaja) <= int(msg.body) and int(kolicinaZaProdaju) > 0):
                    msg2 = spade.message.Message(
                        to="agent@rec.foi.hr",
                        body=msg.body,
                        metadata={
                            "language": "hrvatski",
                            "performative": "inform"})
                    await self.send(msg2)

    async def setup(self):
        analiziraj=self.AnalizirajCijenu(period=5)
        self.add_behaviour(analiziraj) 


class KupiAgent(Agent):
    class KupiKriptovalutu(PeriodicBehaviour):
        async def run(self):
            msg3 = await self.receive()
            if msg3:
                global kolicinaKupnje
                global kolicinaZaProdaju
                global ukupanIznosKupnje
                ukupanIznosKupnje = int(kolicinaKupnje)*int(msg3.body)
                kolicinaZaProdaju = kolicinaKupnje
                print(f"Uspjesna kupovina\nKolicina: {kolicinaKupnje}\nCijena: {msg3.body}\nUkupna vrijednost: {ukupanIznosKupnje}")
                kolicinaKupnje = "0"

    async def setup(self):
        kupi=self.KupiKriptovalutu(period=5)
        self.add_behaviour(kupi)

class ProdajAgent(Agent):
    class ProdajKriptovalutu(PeriodicBehaviour):
        async def run(self):
            msg3 = await self.receive()
            if msg3:
                global kolicinaZaProdaju
                global ukupanIznosProdaje
                ukupanIznosProdaje = int(kolicinaZaProdaju)*int(msg3.body)
                print(f"Uspjesna prodaja\nKolicina: {kolicinaZaProdaju}\nCijena: {msg3.body}\nUkupna vrijednost: {ukupanIznosProdaje}\nProfit: {ukupanIznosProdaje-ukupanIznosKupnje}")
                kolicinaZaProdaju = "0"
            
    async def setup(self):
        prodaj=self.ProdajKriptovalutu(period=5)
        self.add_behaviour(prodaj)


if __name__ == '__main__':

    signalAgent=SignalAgent("smihalic_1@rec.foi.hr", "agentbroj001")
    okruzje=Okruzje("smihalic_2@rec.foi.hr", "agentbroj002")
    kupiAgent=KupiAgent("smihalic_3@rec.foi.hr", "agentbroj003")
    prodajAgent=ProdajAgent("agent@rec.foi.hr", "tajna")

    cijenaKriptovalute = random.randint(48000,51000)

    kolicinaKupnje = input("Unesite kolicinu kriptovalute koju zelite kupiti:\n")
    iznosKupnja = input("Unesite iznos po kojem zelite kupiti kriptovalutu:\n")
    iznosProdaja = input("Unesite iznos po kojem zelite prodati kriptovalutu:\n")
    okruzje.start()
    input("Pokrecem program!\n")
    
    signalAgent.stop()
    okruzje.stop()
    kupiAgent.stop()
    prodajAgent.stop()
    spade.quit_spade()