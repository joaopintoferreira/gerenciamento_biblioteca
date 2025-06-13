# =============================================================================
# services/comentario_service.py
# Serviço para gerenciar comentários e resenhas
# =============================================================================
from datetime import datetime
class ComentarioService:
    def __init__(self, conn):
        self.conn = conn
    '''
    def adicionar_comentario(self, id_usuario, id_livro, texto):
        cursor = self.conn.cursor()
        
        try:
            # Verificar se o usuário já leu o livro
            cursor.execute("""
                SELECT COUNT(*) FROM Emprestimo 
                WHERE Id_Usuario = %s AND Id_Livro = %s AND Devolvido = TRUE
            """, (id_usuario, id_livro))
            
            if cursor.fetchone()[0] == 0:
                print("Você precisa ter lido o livro para comentar.")
                return False
            
            # Adicionar comentário
            cursor.execute("""
                INSERT INTO Comentario (Id_Usuario, Id_Livro, Texto)
                VALUES (%s, %s, %s)
            """, (id_usuario, id_livro, texto))
             # Adicionar pontos ao usuário por comentário
            pontos_por_comentario = 3
            data_comentario = datetime.now().date()
            cursor.execute("""
                INSERT INTO Pontuacao (Id_Usuario, Motivo, Pontos, Data_Pontuacao)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (Id_Usuario)
                DO UPDATE SET Pontos = Pontuacao.Pontos + EXCLUDED.Pontos
            """, (id_usuario, 'Comentário adicionado', pontos_por_comentario, data_comentario))
            self.conn.commit()
            print("Comentário adicionado com sucesso!")
            return True
            
        except Exception as e:
            print(f"Erro ao adicionar comentário: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()
    '''
    def adicionar_comentario(self, id_usuario, id_livro, texto):
        cursor = self.conn.cursor()
        
        try:
            # Verificar se o usuário já leu o livro
            cursor.execute("""
                SELECT 1 FROM Emprestimo 
                WHERE Id_Usuario = %s AND Id_Livro = %s AND Devolvido = TRUE
            """, (id_usuario, id_livro))
            
            if not cursor.fetchone():
                print("Você precisa ter lido o livro para comentar.")
                return False
            
            # Adicionar comentário
            cursor.execute("""
                INSERT INTO Comentario (Id_Usuario, Id_Livro, Texto)
                VALUES (%s, %s, %s)
            """, (id_usuario, id_livro, texto))
            
            # Adicionar pontos ao usuário por comentário
            pontos_por_comentario = 3
            data_comentario = datetime.now().date()
            cursor.execute("""
                INSERT INTO Pontuacao (Id_Usuario, Motivo, Pontos, Data_Pontuacao)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (Id_Usuario)
                DO UPDATE SET Pontos = Pontuacao.Pontos + EXCLUDED.Pontos
            """, (id_usuario, 'Comentário adicionado', pontos_por_comentario, data_comentario))
            
            self.conn.commit()
            print("Comentário adicionado com sucesso!")
            return True
            
        except Exception as e:
            print(f"Erro ao adicionar comentário: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    '''
    def adicionar_resenha(self, id_usuario, id_livro, resenha):
        cursor = self.conn.cursor()
        
        try:
            # Verificar se o usuário já leu o livro
            cursor.execute("""
                SELECT COUNT(*) FROM Emprestimo 
                WHERE Id_Usuario = %s AND Id_Livro = %s AND Devolvido = TRUE
            """, (id_usuario, id_livro))
            
            if cursor.fetchone()[0] == 0:
                print("Você precisa ter lido o livro para escrever uma resenha.")
                return False
            
            # Adicionar ou atualizar resenha
            cursor.execute("""
                INSERT INTO Resenha (Id_Usuario, Id_Livro, Resenha)
                VALUES (%s, %s, %s)
                ON CONFLICT (Id_Usuario, Id_Livro) 
                DO UPDATE SET Resenha = EXCLUDED.Resenha
            """, (id_usuario, id_livro, resenha))
            # Adicionar pontos ao usuário por resenha
            pontos_por_resenha = 15
            data_resenha = datetime.now().date()
            cursor.execute("""
                INSERT INTO Pontuacao (Id_Usuario, Motivo, Pontos, Data_Pontuacao)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (Id_Usuario)
                DO UPDATE SET Pontos = Pontuacao.Pontos + EXCLUDED.Pontos
            """, (id_usuario, 'Resenha escrita', pontos_por_resenha, data_resenha))
            self.conn.commit()
            print("Resenha salva com sucesso!")
            return True
            
        except Exception as e:
            print(f"Erro ao salvar resenha: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()
    '''
    def adicionar_resenha(self, id_usuario, id_livro, resenha):
        cursor = self.conn.cursor()
        
        try:
            # Verificar se o usuário já leu o livro
            cursor.execute("""
                SELECT 1 FROM Emprestimo 
                WHERE Id_Usuario = %s AND Id_Livro = %s AND Devolvido = TRUE
            """, (id_usuario, id_livro))
            
            if not cursor.fetchone():
                print("Você precisa ter lido o livro para escrever uma resenha.")
                return False
            
            # Adicionar ou atualizar resenha
            cursor.execute("""
                INSERT INTO Resenha (Id_Usuario, Id_Livro, Resenha)
                VALUES (%s, %s, %s)
                ON CONFLICT (Id_Usuario, Id_Livro) 
                DO UPDATE SET Resenha = EXCLUDED.Resenha
            """, (id_usuario, id_livro, resenha))
            
            # Adicionar pontos ao usuário por resenha
            pontos_por_resenha = 15
            data_resenha = datetime.now().date()
            cursor.execute("""
                INSERT INTO Pontuacao (Id_Usuario, Motivo, Pontos, Data_Pontuacao)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (Id_Usuario)
                DO UPDATE SET Pontos = Pontuacao.Pontos + EXCLUDED.Pontos
            """, (id_usuario, 'Resenha escrita', pontos_por_resenha, data_resenha))
            
            self.conn.commit()
            print("Resenha salva com sucesso!")
            return True
            
        except Exception as e:
            print(f"Erro ao salvar resenha: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()
        
    def listar_resenhas_livro(self, id_livro):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                SELECT u.Nome, r.Resenha, r.Curtidas
                FROM Resenha r
                JOIN Usuario u ON r.Id_Usuario = u.Id_Usuario
                WHERE r.Id_Livro = %s
                ORDER BY r.Curtidas DESC
            """, (id_livro,))
            resenhas = cursor.fetchall()
            if not resenhas:
                print("Nenhuma resenha encontrada para este livro.")
                return []

            # Obter título do livro
            cursor.execute("SELECT Titulo FROM Livro WHERE Id_Livro = %s", (id_livro,))
            titulo = cursor.fetchone()[0]

            print(f"\n=== RESENHAS - {titulo.upper()} ===")
            for resenha in resenhas:
                print(f"\n📝 {resenha[0]}")
                print(f"⭐ {resenha[2]} Curtidas")
                print(f"📄 {resenha[1]}\n")
            return resenhas
        except Exception as e:
            print(f"Erro ao listar resenhas: {e}")
            return []
        finally:
            cursor.close()

    def curtir_resenha(self, id_usuario, id_livro):
        cursor = self.conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE Resenha 
                SET Curtidas = Curtidas + 1
                WHERE Id_Usuario = %s AND Id_Livro = %s
            """, (id_usuario, id_livro))
            
            if cursor.rowcount == 0:
                print("Resenha não encontrada.")
                return False
            
            self.conn.commit()
            print("Resenha curtida!")
            return True
            
        except Exception as e:
            print(f"Erro ao curtir resenha: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()