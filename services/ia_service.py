'''
# =============================================================================
# services/ia_service.py
# Serviço de IA para recomendações
# =============================================================================

import openai
import os

class IAService:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')
    
    def recomendar_livros(self, conn, id_usuario):
        cursor = conn.cursor()
        
        # Obter histórico do usuário
        cursor.execute("""
            SELECT l.Titulo, l.Ano_Publicacao, a.Nome as Autor
            FROM Emprestimo e
            JOIN Livro l ON e.Id_Livro = l.Id_Livro
            JOIN Co_Autor ca ON l.Id_Livro = ca.Id_Livro
            JOIN Autor a ON ca.Id_Autor = a.Id_Autor
            WHERE e.Id_Usuario = %s AND e.Devolvido = TRUE
            ORDER BY e.Data_Devolucao DESC
            LIMIT 5
        """, (id_usuario,))
        
        historico = cursor.fetchall()
        cursor.close()
        
        if not historico:
            return "Você ainda não tem histórico de empréstimos. Explore nossa biblioteca!"
        
        # Preparar contexto para IA
        livros_lidos = ", ".join([f"{livro[0]} de {livro[2]}" for livro in historico])
        
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Você é um bibliotecário especialista em recomendações literárias."},
                    {"role": "user", "content": f"Com base nos livros que o usuário já leu: {livros_lidos}, recomende 3 livros similares da literatura brasileira, explicando brevemente o motivo de cada recomendação."}
                ],
                max_tokens=300
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Erro ao gerar recomendação: {e}"
    
    def sugerir_comentario_resenha(self, conn, id_usuario, id_livro):
        cursor = conn.cursor()
        
        # Obter informações do livro
        cursor.execute("""
            SELECT l.Titulo, a.Nome as Autor
            FROM Livro l
            JOIN Co_Autor ca ON l.Id_Livro = ca.Id_Livro
            JOIN Autor a ON ca.Id_Autor = a.Id_Autor
            WHERE l.Id_Livro = %s
        """, (id_livro,))
        
        livro_info = cursor.fetchone()
        cursor.close()
        
        if not livro_info:
            return "Livro não encontrado."
        
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Você é um assistente que ajuda usuários a escrever comentários e resenhas de livros."},
                    {"role": "user", "content": f"Sugira 3 perguntas reflexivas que um leitor poderia responder ao comentar sobre o livro '{livro_info[0]}' de {livro_info[1]}, para ajudá-lo a escrever uma boa resenha."}
                ],
                max_tokens=200
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Erro ao gerar sugestão: {e}"
'''
# =============================================================================
# services/ia_service.py
# Serviço de IA para recomendações
# =============================================================================
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
import os

class IAService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def recomendar_livros(self, conn, id_usuario):
        try:
            cursor = conn.cursor()

            # Obter histórico do usuário
            cursor.execute("""
                SELECT l.Titulo, l.Ano_Publicacao, a.Nome as Autor
                FROM Emprestimo e
                JOIN Livro l ON e.Id_Livro = l.Id_Livro
                JOIN Co_Autor ca ON l.Id_Livro = ca.Id_Livro
                JOIN Autor a ON ca.Id_Autor = a.Id_Autor
                WHERE e.Id_Usuario = %s AND e.Devolvido = TRUE
                ORDER BY e.Data_Devolucao DESC
                LIMIT 5
            """, (id_usuario,))

            historico = cursor.fetchall()
            cursor.close()

            if not historico:
                return "Você ainda não tem histórico de empréstimos. Explore nossa biblioteca!"

            livros_lidos = ", ".join([f"{livro[0]} de {livro[2]}" for livro in historico])

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Você é um bibliotecário especialista em recomendações literárias."},
                    {"role": "user", "content": f"Com base nos livros que o usuário já leu: {livros_lidos}, recomende 3 livros similares da literatura brasileira, explicando brevemente o motivo de cada recomendação."}
                ],
                temperature=0.7,
                max_tokens=300
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            return f"Erro ao gerar recomendação: {e}"

    def sugerir_comentario_resenha(self, conn, id_usuario, id_livro):
        try:
            cursor = conn.cursor()

            # Obter informações do livro
            cursor.execute("""
                SELECT l.Titulo, a.Nome as Autor
                FROM Livro l
                JOIN Co_Autor ca ON l.Id_Livro = ca.Id_Livro
                JOIN Autor a ON ca.Id_Autor = a.Id_Autor
                WHERE l.Id_Livro = %s
            """, (id_livro,))

            livro_info = cursor.fetchone()
            cursor.close()

            if not livro_info:
                return "Livro não encontrado."

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Você é um assistente que ajuda usuários a escrever comentários e resenhas de livros."},
                    {"role": "user", "content": f"Sugira 3 perguntas reflexivas que um leitor poderia responder ao comentar sobre o livro '{livro_info[0]}' de {livro_info[1]}, para ajudá-lo a escrever uma boa resenha."}
                ],
                temperature=0.7,
                max_tokens=200
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            return f"Erro ao gerar sugestão: {e}"
