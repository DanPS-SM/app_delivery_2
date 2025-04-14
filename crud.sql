-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Tempo de geração: 02-Abr-2025 às 17:50
-- Versão do servidor: 8.2.0
-- versão do PHP: 7.4.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `crud`
--

-- --------------------------------------------------------

--
-- Estrutura da tabela `clientes`
--

DROP TABLE IF EXISTS `clientes`;
CREATE TABLE IF NOT EXISTS `clientes` (
  `id_cliente` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `endereco` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `telefone` varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id_cliente`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `clientes`
--

INSERT INTO `clientes` (`id_cliente`, `nome`, `endereco`, `telefone`) VALUES
(1, 'Fernando Pessoa', 'Rua da Alegria', '9198765432'),
(6, 'Luis Carlos', 'Rodovia Br-316', '9999888888'),
(8, 'Maria Jose', 'Alame A, 13', '91998563312');

-- --------------------------------------------------------

--
-- Estrutura da tabela `entregadores`
--

DROP TABLE IF EXISTS `entregadores`;
CREATE TABLE IF NOT EXISTS `entregadores` (
  `id_entregador` int NOT NULL AUTO_INCREMENT,
  `cpf` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `nome` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `endereco` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `telefone` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id_entregador`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `entregadores`
--

INSERT INTO `entregadores` (`id_entregador`, `cpf`, `nome`, `endereco`, `telefone`) VALUES
(1, '12088730222', 'Alberto Roberto', 'Rua 10', '9199874856'),
(4, '12345678912', 'José Rualdo Lopes', 'Avenida 3 poderes, 12', '9197823'),
(9, '12088730222', 'Alberto Roberto junior', 'Rua 10', '9199874856'),
(11, '123456789', 'Jose', 'Rua aaaaaa', '88999999666'),
(12, '123132323', 'Gordo', 'WSDSD', '314334');

-- --------------------------------------------------------

--
-- Estrutura da tabela `pedidos`
--

DROP TABLE IF EXISTS `pedidos`;
CREATE TABLE IF NOT EXISTS `pedidos` (
  `id_pedido` int NOT NULL AUTO_INCREMENT,
  `data` date NOT NULL,
  `hora` time NOT NULL,
  `total` float NOT NULL,
  `status` int NOT NULL,
  `forma_pagamento` int NOT NULL,
  `endereco_entrega` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `cliente_id` int NOT NULL,
  `entregador_id` int NOT NULL,
  PRIMARY KEY (`id_pedido`),
  KEY `fk_clientes` (`cliente_id`),
  KEY `fk_entregadores` (`entregador_id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `pedidos`
--

INSERT INTO `pedidos` (`id_pedido`, `data`, `hora`, `total`, `status`, `forma_pagamento`, `endereco_entrega`, `cliente_id`, `entregador_id`) VALUES
(33, '2025-03-27', '15:26:28', 42.5, 0, 1, 'Rua A, 1000', 6, 1),
(34, '2025-03-27', '16:52:40', 11.6, 0, 1, 'Rua do beco', 1, 4),
(35, '2025-03-27', '17:14:57', 13.6, 0, 3, 'Rua da Lua, 13', 1, 1),
(36, '2025-03-27', '17:19:36', 105, 0, 4, 'Travesa das dores', 6, 1),
(37, '2025-03-27', '17:24:42', 110.8, 0, 1, 'Travessa 14 de março', 1, 1),
(38, '2025-03-27', '17:28:02', 21.4, 0, 1, 'Rua Carlos Gomes', 6, 1),
(39, '2025-03-27', '17:30:39', 48.3, 0, 3, 'Rua C. 10', 1, 4),
(40, '2025-03-27', '17:34:06', 21.4, 0, 2, 'Rua Jota', 1, 1),
(41, '2025-03-27', '17:37:20', 19, 0, 3, 'Avenida Boa', 6, 1),
(42, '2025-03-27', '19:06:00', 13.6, 0, 3, 'Rua nova 1434', 1, 1);

-- --------------------------------------------------------

--
-- Estrutura da tabela `pedido_produto`
--

DROP TABLE IF EXISTS `pedido_produto`;
CREATE TABLE IF NOT EXISTS `pedido_produto` (
  `id_pedido_produto` int NOT NULL AUTO_INCREMENT,
  `quantidade` int NOT NULL,
  `produto_id` int NOT NULL,
  `pedido_id` int NOT NULL,
  PRIMARY KEY (`id_pedido_produto`),
  KEY `fk_produtos` (`produto_id`),
  KEY `fk_pedidos` (`pedido_id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `pedido_produto`
--

INSERT INTO `pedido_produto` (`id_pedido_produto`, `quantidade`, `produto_id`, `pedido_id`) VALUES
(15, 2, 8, 34),
(18, 1, 2, 36),
(19, 1, 6, 39),
(20, 5, 7, 39),
(21, 2, 6, 42),
(22, 1, 8, 42),
(23, 5, 7, 33),
(24, 2, 1, 40),
(25, 1, 6, 40),
(29, 1, 1, 38),
(30, 2, 6, 38),
(31, 1, 8, 38),
(32, 2, 7, 41),
(33, 1, 8, 41),
(34, 2, 6, 35),
(35, 1, 8, 35);

-- --------------------------------------------------------

--
-- Estrutura da tabela `produtos`
--

DROP TABLE IF EXISTS `produtos`;
CREATE TABLE IF NOT EXISTS `produtos` (
  `id_produto` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `descricao` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `fornecedor` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `estoque` int NOT NULL,
  `preco_unitario` float NOT NULL,
  PRIMARY KEY (`id_produto`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `produtos`
--

INSERT INTO `produtos` (`id_produto`, `nome`, `descricao`, `fornecedor`, `estoque`, `preco_unitario`) VALUES
(1, 'Água Mineral', 'Galão de água mineral 20 litros', 'Belagua', 1000, 7.8),
(2, 'Gás de Cozinha', 'Botijão de gás butano 13kg', 'Liquigás', 500, 105.1),
(6, 'Refrigerante 2lts', 'Coca-cola e sabores 2 litros', 'ambev', 120, 5.8),
(7, 'Cerveja Lata 269ml', 'Cerveja lata 269ml, skol, amstel, bhrama', 'ambev', 50, 8.5),
(8, 'Pastilhas Halls', 'Pastilhas halls e sabores', 'adams', 30, 2),
(9, 'Jujuba', 'doce', 'adams', 30, 5.5);

--
-- Restrições para despejos de tabelas
--

--
-- Limitadores para a tabela `pedidos`
--
ALTER TABLE `pedidos`
  ADD CONSTRAINT `fk_clientes` FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`id_cliente`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_entregadores` FOREIGN KEY (`entregador_id`) REFERENCES `entregadores` (`id_entregador`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Limitadores para a tabela `pedido_produto`
--
ALTER TABLE `pedido_produto`
  ADD CONSTRAINT `fk_pedidos` FOREIGN KEY (`pedido_id`) REFERENCES `pedidos` (`id_pedido`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_produtos` FOREIGN KEY (`produto_id`) REFERENCES `produtos` (`id_produto`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
