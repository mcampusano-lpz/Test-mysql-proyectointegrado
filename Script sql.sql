-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema RGbeauty
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema RGbeauty
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `RGbeauty` DEFAULT CHARACTER SET utf8 ;
USE `RGbeauty` ;

-- -----------------------------------------------------
-- Table `RGbeauty`.`Usuarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `RGbeauty`.`Usuarios` (
  `idUsuarios` INT NOT NULL AUTO_INCREMENT,
  `nombre` LONGTEXT NOT NULL,
  `email` LONGTEXT NOT NULL,
  `contrasena` LONGTEXT NOT NULL,
  `rol` LONGTEXT NOT NULL,
  PRIMARY KEY (`idUsuarios`),
  UNIQUE INDEX `idUsuarios_UNIQUE` (`idUsuarios` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `RGbeauty`.`Productos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `RGbeauty`.`Productos` (
  `idProductos` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NOT NULL,
  `marca` VARCHAR(45) NOT NULL,
  `descripcion` LONGTEXT NOT NULL,
  `stock_actual` INT NOT NULL,
  `fecha_vencimiento` DATE NOT NULL,
  `esta_bloqueado` TINYINT NOT NULL,
  PRIMARY KEY (`idProductos`),
  UNIQUE INDEX `idProductos_UNIQUE` (`idProductos` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `RGbeauty`.`Auditoria_edicion`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `RGbeauty`.`Auditoria_edicion` (
  `idAuditoria` INT NOT NULL AUTO_INCREMENT,
  `cantidad_ajustada` INT NOT NULL,
  `fecha_ajuste` DATE NOT NULL,
  `motivo` LONGTEXT NOT NULL,
  `Productos_idProductos` INT NULL,
  `Usuarios_idUsuarios` INT NULL,
  PRIMARY KEY (`idAuditoria`),
  UNIQUE INDEX `idAuditoria_UNIQUE` (`idAuditoria` ASC) VISIBLE,
  INDEX `fk_Auditoria_Productos1_idx` (`Productos_idProductos` ASC) VISIBLE,
  INDEX `fk_Auditoria_Usuarios1_idx` (`Usuarios_idUsuarios` ASC) VISIBLE,
  CONSTRAINT `fk_Auditoria_Productos1`
    FOREIGN KEY (`Productos_idProductos`)
    REFERENCES `RGbeauty`.`Productos` (`idProductos`)
    ON DELETE SET NULL
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Auditoria_Usuarios1`
    FOREIGN KEY (`Usuarios_idUsuarios`)
    REFERENCES `RGbeauty`.`Usuarios` (`idUsuarios`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `RGbeauty`.`Auditoria_registro`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `RGbeauty`.`Auditoria_registro` (
  `idAuditoria_registro` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `cantidad_registrada` INT NOT NULL,
  `fecha_registro` DATE NOT NULL,
  `observacion` LONGTEXT NULL,
  `Usuarios_idUsuarios` INT NULL,
  `Productos_idProductos` INT NULL,
  PRIMARY KEY (`idAuditoria_registro`),
  UNIQUE INDEX `idAuditoria_registro_UNIQUE` (`idAuditoria_registro` ASC) VISIBLE,
  INDEX `fk_Auditoria_registro_Usuarios1_idx` (`Usuarios_idUsuarios` ASC) VISIBLE,
  INDEX `fk_Auditoria_registro_Productos1_idx` (`Productos_idProductos` ASC) VISIBLE,
  CONSTRAINT `fk_Auditoria_registro_Usuarios1`
    FOREIGN KEY (`Usuarios_idUsuarios`)
    REFERENCES `RGbeauty`.`Usuarios` (`idUsuarios`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Auditoria_registro_Productos1`
    FOREIGN KEY (`Productos_idProductos`)
    REFERENCES `RGbeauty`.`Productos` (`idProductos`)
    ON DELETE SET NULL
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
