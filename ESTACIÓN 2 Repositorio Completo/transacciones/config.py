"""
config.py
Parámetros de negocio del sistema de gestión de transacciones.

Se dejan en un único lugar para que sean fáciles de cambiar sin tocar la
lógica de las clases (SRP: este módulo solo guarda configuración).
"""

# Tasa de interés mensual aplicada a los créditos (0.018 = 1.8 % mensual).
TASA_INTERES_CREDITO = 0.018

# Comisión fija en pesos que se cobra por cada débito.
COMISION_FIJA_DEBITO = 6500
