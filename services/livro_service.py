class LivroService:
    def __init__(self, conn):
        self.conn = conn

    def adicionar_livro(self, titulo, ano_publicacao, id_editora, id_categoria):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Livro (Titulo, Ano_Publicacao, Id_Editora, Id_Categoria)
                VALUES (%s, %s, %s, %s)
            """, (titulo, ano_publicacao, id_editora, id_categoria))
            self.conn.commit()
            print("Livro adicionado com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao adicionar livro: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    def atualizar_livro(self, id_livro, titulo=None, ano_publicacao=None, id_editora=None, id_categoria=None):
        cursor = self.conn.cursor()
        try:
            # Construir a consulta SQL dinamicamente com base nos parâmetros fornecidos
            updates = []
            params = []
            if titulo is not None:
                updates.append("Titulo = %s")
                params.append(titulo)
            if ano_publicacao is not None:
                updates.append("Ano_Publicacao = %s")
                params.append(ano_publicacao)
            if id_editora is not None:
                updates.append("Id_Editora = %s")
                params.append(id_editora)
            if id_categoria is not None:
                updates.append("Id_Categoria = %s")
                params.append(id_categoria)

            if not updates:
                print("Nenhum campo para atualizar foi fornecido.")
                return False

            params.append(id_livro)
            update_query = f"UPDATE Livro SET {', '.join(updates)} WHERE Id_Livro = %s"
            cursor.execute(update_query, params)
            self.conn.commit()
            print("Livro atualizado com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao atualizar livro: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    def remover_livro(self, id_livro):
        cursor = self.conn.cursor()
        try:
            cursor.execute("DELETE FROM Livro WHERE Id_Livro = %s", (id_livro,))
            self.conn.commit()
            print("Livro removido com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao remover livro: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()
   
    def listar_livros(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                SELECT Id_Livro, Titulo, Ano_Publicacao, Id_Editora, Id_Categoria, Quantidade_Exemplares
                FROM Livro
            """)
            livros = cursor.fetchall()

            if not livros:
                print("Nenhum livro encontrado.")
                return []

            print("\n=== LISTA DE LIVROS ===")
            for livro in livros:
                print(f"ID: {livro[0]}, Título: {livro[1]}, Ano: {livro[2]}, Editora ID: {livro[3]}, Categoria ID: {livro[4]}, Quantidade de Exemplares: {livro[5]}")

            return livros
        except Exception as e:
            print(f"Erro ao listar livros: {e}")
            return []
        finally:
            cursor.close()

    def buscar_livro_por_id(self, id_livro):
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT * FROM Livro WHERE Id_Livro = %s", (id_livro,))
            livro = cursor.fetchone()
            if not livro:
                print("Livro não encontrado.")
                return None
            print(f"ID: {livro[0]}, Título: {livro[1]}, Ano: {livro[3]}, Editora ID: {livro[4]}, Categoria ID: {livro[5]}")
            return livro
        except Exception as e:
            print(f"Erro ao buscar livro: {e}")
            return None
        finally:
            cursor.close()
