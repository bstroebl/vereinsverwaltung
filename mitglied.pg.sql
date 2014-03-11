
-- -----------------------------------------------------
-- Table "verein"."beitragsgruppe"
-- -----------------------------------------------------
CREATE  TABLE  "verein"."beitragsgruppe" (
  "id" INTEGER NOT NULL ,
  "beitragsgruppe" VARCHAR(255) NOT NULL ,
  "beitrag_nach_satzung" INTEGER NOT NULL ,
  PRIMARY KEY ("id") )
;


-- -----------------------------------------------------
-- Table "verein"."mitgliedsgruppe"
-- -----------------------------------------------------
CREATE  TABLE  "verein"."mitgliedsgruppe" (
  "id" INTEGER NOT NULL ,
  "mitgliedsgruppe" VARCHAR(255) NOT NULL ,
  PRIMARY KEY ("id") )
;


-- -----------------------------------------------------
-- Table "verein"."austrittsgrund"
-- -----------------------------------------------------
CREATE  TABLE  "verein"."austrittsgrund" (
  "id" INTEGER NOT NULL ,
  "austrittsgrund" VARCHAR(255) NOT NULL ,
  PRIMARY KEY ("id") )
;


-- -----------------------------------------------------
-- Table "verein"."zahlungsart"
-- -----------------------------------------------------
CREATE  TABLE  "verein"."zahlungsart" (
  "id" INTEGER NOT NULL ,
  "zahlungsart" VARCHAR(255) NOT NULL ,
  PRIMARY KEY ("id") )
;


-- -----------------------------------------------------
-- Table "verein"."land"
-- -----------------------------------------------------
CREATE  TABLE  "verein"."land" (
  "id" INTEGER NOT NULL ,
  "land" VARCHAR(255) NOT NULL ,
  PRIMARY KEY ("id") )
;


-- -----------------------------------------------------
-- Table "verein"."ort"
-- -----------------------------------------------------
CREATE  TABLE  "verein"."ort" (
  "id" INTEGER NOT NULL ,
  "ort" VARCHAR(255) NOT NULL ,
  "plz" VARCHAR(8) NOT NULL ,
  "land_id" INTEGER NOT NULL ,
  PRIMARY KEY ("id") ,
  CONSTRAINT "fk_ort_land1"
    FOREIGN KEY ("land_id" )
    REFERENCES "verein"."land" ("id" )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
;

CREATE INDEX "idx_fk_ort_land1" ON "verein"."ort" ("land_id") ;


-- -----------------------------------------------------
-- Table "verein"."bank"
-- -----------------------------------------------------
CREATE  TABLE  "verein"."bank" (
  "id" INTEGER NOT NULL ,
  "bank" VARCHAR(255) NOT NULL ,
  PRIMARY KEY ("id") )
;


-- -----------------------------------------------------
-- Table "verein"."mitglied"
-- -----------------------------------------------------
CREATE  TABLE  "verein"."mitglied" (
  "id" INTEGER NOT NULL ,
  "mitgliedsname" VARCHAR(255) NOT NULL ,
  "mitgliedsgruppe_id" INTEGER NOT NULL ,
  "eintrittsdatum" DATE NOT NULL ,
  "letzte_aenderung" TIMESTAMP NOT NULL ,
  "beitragsgruppe_id" INTEGER NOT NULL ,
  "individueller_beitrag" INTEGER NULL ,
  "austrittsdatum" DATE NULL ,
  "austrittsgrund_id" INTEGER NULL ,
  "strasse" VARCHAR(255) NULL ,
  "hnr" INTEGER NULL ,
  "hnrzusatz" VARCHAR(8) NULL ,
  "adresszusatz" VARCHAR(64) NULL ,
  "ort_id" INTEGER NULL ,
  "zahlungsart_id" INTEGER NULL ,
  "kontonummer" INTEGER NULL ,
  "kontoinhaber" INTEGER NULL ,
  "blz" INTEGER NULL ,
  PRIMARY KEY ("id") ,
  CONSTRAINT "fk_mitglied_beitragsgruppe1"
    FOREIGN KEY ("beitragsgruppe_id" )
    REFERENCES "verein"."beitragsgruppe" ("id" )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT "fk_mitglied_mitgliedsgruppe1"
    FOREIGN KEY ("mitgliedsgruppe_id" )
    REFERENCES "verein"."mitgliedsgruppe" ("id" )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT "fk_mitglied_austrittsgrund1"
    FOREIGN KEY ("austrittsgrund_id" )
    REFERENCES "verein"."austrittsgrund" ("id" )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT "fk_mitglied_zahlungsart1"
    FOREIGN KEY ("zahlungsart_id" )
    REFERENCES "verein"."zahlungsart" ("id" )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT "fk_mitglied_ort1"
    FOREIGN KEY ("ort_id" )
    REFERENCES "verein"."ort" ("id" )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT "fk_mitglied_bank1"
    FOREIGN KEY ("blz" )
    REFERENCES "verein"."bank" ("id" )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
;

CREATE INDEX "idx_fk_mitglied_beitragsgruppe1" ON "verein"."mitglied" ("beitragsgruppe_id") ;

CREATE INDEX "idx_fk_mitglied_mitgliedsgruppe1" ON "verein"."mitglied" ("mitgliedsgruppe_id") ;

CREATE INDEX "idx_fk_mitglied_austrittsgrund1" ON "verein"."mitglied" ("austrittsgrund_id") ;

CREATE INDEX "idx_fk_mitglied_zahlungsart1" ON "verein"."mitglied" ("zahlungsart_id") ;

CREATE INDEX "idx_fk_mitglied_ort1" ON "verein"."mitglied" ("ort_id") ;

CREATE INDEX "idx_fk_mitglied_bank1" ON "verein"."mitglied" ("blz") ;


-- -----------------------------------------------------
-- Table "verein"."anrede"
-- -----------------------------------------------------
CREATE  TABLE  "verein"."anrede" (
  "id" INTEGER NOT NULL ,
  "anrede" VARCHAR(255) NOT NULL ,
  PRIMARY KEY ("id") )
;


-- -----------------------------------------------------
-- Table "verein"."hinweis_email"
-- -----------------------------------------------------
CREATE  TABLE  "verein"."hinweis_email" (
  "id" INTEGER NOT NULL ,
  "hinweis" VARCHAR(255) NOT NULL ,
  PRIMARY KEY ("id") )
;


-- -----------------------------------------------------
-- Table "verein"."hinweis_telefonfax"
-- -----------------------------------------------------
CREATE  TABLE  "verein"."hinweis_telefonfax" (
  "id" INTEGER NOT NULL ,
  "hinweis" VARCHAR(255) NOT NULL ,
  PRIMARY KEY ("id") )
;


-- -----------------------------------------------------
-- Table "verein"."telefonfax"
-- -----------------------------------------------------
CREATE  TABLE  "verein"."telefonfax" (
  "id" serial NOT NULL,
  "mitglied_id" INTEGER NOT NULL ,
  "nummer" VARCHAR(64) NOT NULL ,
  "hinweis_id" INTEGER NOT NULL ,
  PRIMARY KEY ("id") ,
  CONSTRAINT "fk_mitglied_has_telefonfax_mitglied1"
    FOREIGN KEY ("mitglied_id" )
    REFERENCES "verein"."mitglied" ("id" )
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT "fk_telefonfax_hinweis_telefon1"
    FOREIGN KEY ("hinweis_id" )
    REFERENCES "verein"."hinweis_telefon" ("id" )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
;

CREATE INDEX "idx_fk_mitglied_has_telefonfax_mitglied1" ON "verein"."telefonnummer" ("mitglied_id") ;

CREATE INDEX "idx_fk_telefonfax_hinweis_telefon1" ON "verein"."telefonnummer" ("hinweis_id") ;


-- -----------------------------------------------------
-- Table "verein"."email"
-- -----------------------------------------------------
CREATE  TABLE  "verein"."email" (
  "id" serial NOT NULL,
  "mitglied_id" INTEGER NOT NULL ,
  "email" VARCHAR(255) NOT NULL ,
  "hinweis_id" INTEGER NOT NULL ,
  PRIMARY KEY ("id") ,
  CONSTRAINT "fk_mitglied_has_email_mitglied1"
    FOREIGN KEY ("mitglied_id" )
    REFERENCES "verein"."mitglied" ("id" )
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT "fk_mitglied_has_email_hinweis1"
    FOREIGN KEY ("hinweis_id" )
    REFERENCES "verein"."hinweis_email" ("id" )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
;

CREATE INDEX "idx_fk_mitglied_has_email_mitglied1" ON "verein"."email" ("mitglied_id") ;

CREATE INDEX "idx_fk_mitglied_has_email_hinweis1" ON "verein"."email" ("hinweis_id") ;


-- -----------------------------------------------------
-- Table "verein"."schreibenart"
-- -----------------------------------------------------
CREATE  TABLE  "verein"."schreibenart" (
  "id" INTEGER NOT NULL ,
  "schreibenart" VARCHAR(255) NOT NULL ,
  PRIMARY KEY ("id") )
;


-- -----------------------------------------------------
-- Table "verein"."schreiben"
-- -----------------------------------------------------
CREATE  TABLE  "verein"."schreiben" (
  "id" INTEGER NOT NULL ,
  "erzeugt" TIMESTAMP NOT NULL ,
  "mitglied_id" INTEGER NOT NULL ,
  "schreiben_art_id" INTEGER NOT NULL ,
  "inhalt" VARCHAR(255) NULL ,
  PRIMARY KEY ("id") ,
  CONSTRAINT "fk_schreiben_mitglied1"
    FOREIGN KEY ("mitglied_id" )
    REFERENCES "verein"."mitglied" ("id" )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT "fk_schreiben_schreiben_art1"
    FOREIGN KEY ("schreiben_art_id" )
    REFERENCES "verein"."schreibenart" ("id" )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
;

CREATE INDEX "idx_fk_schreiben_mitglied1" ON "verein"."schreiben" ("mitglied_id") ;

CREATE INDEX "idx_fk_schreiben_schreiben_art1" ON "verein"."schreiben" ("schreiben_art_id") ;


-- -----------------------------------------------------
-- Table "verein"."mitglied_natuerlich"
-- -----------------------------------------------------
CREATE  TABLE  "verein"."mitglied_natuerlich" (
  "mitglied_id" INTEGER NOT NULL ,
  "anrede_id" INTEGER NOT NULL ,
  "titel" VARCHAR(255) NULL ,
  "vorname" VARCHAR(255) NOT NULL ,
  "namenszusatz" VARCHAR(255) NULL ,
  "geburtsdatum" DATE NOT NULL ,
  "hauptmitglied_id" INTEGER NULL ,
  PRIMARY KEY ("mitglied_id") ,
  CONSTRAINT "fk_mitglied_natuerlich_mitglied1"
    FOREIGN KEY ("mitglied_id" )
    REFERENCES "verein"."mitglied" ("id" )
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT "fk_mitglied_natuerlich_mitglied_natuerlich1"
    FOREIGN KEY ("hauptmitglied_id" )
    REFERENCES "verein"."mitglied_natuerlich" ("mitglied_id" )
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT "fk_mitglied_natuerlich_anrede1"
    FOREIGN KEY ("anrede_id" )
    REFERENCES "verein"."anrede" ("id" )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
;

CREATE INDEX "idx_fk_mitglied_natuerlich_mitglied1" ON "verein"."mitglied_natuerlich" ("mitglied_id") ;

CREATE INDEX "idx_fk_mitglied_natuerlich_mitglied_natuerlich1" ON "verein"."mitglied_natuerlich" ("hauptmitglied_id") ;

CREATE INDEX "idx_fk_mitglied_natuerlich_anrede1" ON "verein"."mitglied_natuerlich" ("anrede_id") ;


-- -----------------------------------------------------
-- Table "verein"."mitglied_juristisch"
-- -----------------------------------------------------
CREATE  TABLE  "verein"."mitglied_juristisch" (
  "mitglied_id" INTEGER NOT NULL ,
  "ansprechpartner" VARCHAR(255) NOT NULL ,
  PRIMARY KEY ("mitglied_id") ,
  CONSTRAINT "fk_mitglied_natuerlich_mitglied10"
    FOREIGN KEY ("mitglied_id" )
    REFERENCES "verein"."mitglied" ("id" )
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
;

CREATE INDEX "idx_fk_mitglied_juristisch_mitglied1" ON "verein"."mitglied_juristisch" ("mitglied_id") ;

-- -----------------------------------------------------
-- Table "verein"."hinweis_zahlung"
-- -----------------------------------------------------
CREATE  TABLE "verein"."hinweis_zahlung" (
  "id" INTEGER NOT NULL ,
  "hinweis" VARCHAR(255) NOT NULL ,
  PRIMARY KEY ("id") )
  ;

-- -----------------------------------------------------
-- Table "verein"."zahlung"
-- -----------------------------------------------------
CREATE  TABLE  "verein"."zahlung" (
  "id" serial NOT NULL ,
  "mitglied_id" INTEGER NOT NULL ,
  "betrag" REAL NOT NULL ,
  "zahldatum" DATE NOT NULL ,
  "hinweis_zahlungen_id" INTEGER NOT NULL ,
  PRIMARY KEY ("id") ,
  CONSTRAINT "fk_zahlungen_mitglied1"
    FOREIGN KEY ("mitglied_id" )
    REFERENCES "verein"."mitglied" ("id" )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT "fk_zahlungen_hinweis_zahlungen1"
    FOREIGN KEY ("hinweis_zahlungen_id" )
    REFERENCES "verein"."hinweis_zahlungen" ("id" )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION))
;

CREATE INDEX "idx_fk_zahlungen_mitglied1" ON "verein"."zahlungen" ("mitglied_id") ;
CREATE INDEX "idx_fk_zahlungen_hinweis_zahlungen1" ON "verein"."zahlungen" ("hinweis_zahlungen_id") ;

CREATE OR REPLACE RULE _update AS
    ON UPDATE TO zahlungen DO INSTEAD NOTHING;



