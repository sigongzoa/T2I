from decimal import Decimal

TYPE=(
    (Decimal('1'), '무관'),
    (Decimal('2'), '한식'),
    (Decimal('3'), '중식'),
    (Decimal('4'), '일식'),
    (Decimal('5'), '양식'),
    (Decimal('6'), '기타'),
)
PRICE=(
    (Decimal('1'), '무관'),
    (Decimal('2'), '10000원 이내'),
    (Decimal('3'), '10000원 - 15000원'),
    (Decimal('4'), '15000원 - 20000원'),
    (Decimal('5'), '20000원 이상'),
)
EXP=(
    (Decimal('1'),'무관'),
    (Decimal('2'),'안전한 추천'),
    (Decimal('3'),'도전적 추천'),
)
DISTANCE=(
    (Decimal('1'), '무관'),
    (Decimal('2'), '5분 이내'),
    (Decimal('3'), '10분 이내'),
    (Decimal('4'), '15분 이내'),
    (Decimal('5'), '20분 이내'),
    (Decimal('6'), '25분 이내'),
)
