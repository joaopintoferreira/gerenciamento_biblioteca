# =============================================================================
# services/reserva_service.py
# Serviço para gerenciar reservas
# =============================================================================

from datetime import datetime

class ReservaService:
    def __init__(self, conn):
        self.conn = conn
    
    def fazer_reserva(self, id_usuario, id_livro):
        cursor = self.conn.cursor()
        
        try:
            # Verificar se o livro existe e está emprestado
            cursor.execute("SELECT Status FROM Livro WHERE Id_Livro = %s", (id_livro,))
            livro_status = cursor.fetchone()
            
            if not livro_status:
                print("Livro não encontrado.")
                return False
            
            if livro_status[0] == 'disponível':
                print("Livro está disponível. Realize um empréstimo direto.")
                return False
            
            # Verificar se usuário já tem reserva ativa para este livro
            cursor.execute("""
                SELECT Id_Reserva FROM Reserva 
                WHERE Id_Usuario = %s AND Id_Livro = %s AND Status = 'ativo'
            """, (id_usuario, id_livro))
            
            if cursor.fetchone():
                print("Você já possui uma reserva ativa para este livro.")
                return False
            
            # Criar reserva
            data_reserva = datetime.now().date()
            cursor.execute("""
                INSERT INTO Reserva (Id_Usuario, Id_Livro, Data, Status)
                VALUES (%s, %s, %s, 'ativo')
            """, (id_usuario, id_livro, data_reserva))
            
            self.conn.commit()
            print("Reserva realizada com sucesso! Você será notificado quando o livro estiver disponível.")
            return True
            
        except Exception as e:
            print(f"Erro ao fazer reserva: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()
    
    def cancelar_reserva(self, id_reserva):
        cursor = self.conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE Reserva SET Status = 'cancelado' 
                WHERE Id_Reserva = %s AND Status = 'ativo'
            """, (id_reserva,))
            
            if cursor.rowcount == 0:
                print("Reserva não encontrada ou já cancelada.")
                return False
            
            self.conn.commit()
            print("Reserva cancelada com sucesso.")
            return True
            
        except Exception as e:
            print(f"Erro ao cancelar reserva: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    def excluir_reserva(self, id_reserva):
        cursor = self.conn.cursor()
        try:
            # Verificar se a reserva existe
            cursor.execute("SELECT Id_Reserva FROM Reserva WHERE Id_Reserva = %s", (id_reserva,))
            reserva = cursor.fetchone()

            if not reserva:
                print("Reserva não encontrada.")
                return False

            # Excluir a reserva
            cursor.execute("DELETE FROM Reserva WHERE Id_Reserva = %s", (id_reserva,))
            self.conn.commit()
            print("Reserva excluída com sucesso!")
            return True

        except Exception as e:
            print(f"Erro ao excluir reserva: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()
            
    def listar_reservas_usuario(self, id_usuario):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT r.Id_Reserva, l.Titulo, a.Nome as Autor, r.Data, r.Status
            FROM Reserva r
            JOIN Livro l ON r.Id_Livro = l.Id_Livro
            JOIN Co_Autor ca ON l.Id_Livro = ca.Id_Livro
            JOIN Autor a ON ca.Id_Autor = a.Id_Autor
            WHERE r.Id_Usuario = %s
            ORDER BY r.Data DESC
        """, (id_usuario,))
        
        reservas = cursor.fetchall()
        cursor.close()
        
        if not reservas:
            print("Nenhuma reserva encontrada.")
            return []
        
        print("\n=== SUAS RESERVAS ===")
        for reserva in reservas:
            status_emoji = "🟢" if reserva[4] == 'ativo' else "🔴"
            print(f"{status_emoji} {reserva[1]} - {reserva[2]} (Data: {reserva[3]}) - {reserva[4]}")
        
        return reservas