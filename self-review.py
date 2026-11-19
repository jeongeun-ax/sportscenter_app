import psycopg
from psycopg.rows import dict_row

# DSN : Data Source Name
DSN = "host=localhost port=5432 dbname=sportscenter user=postgres password=admin1234"

MONTH = "2026-11"

LIST_SQL = """
SELECT DISTINCT c.course_id, s.sport_name, c.course_name, c.class_days, c.fee
FROM courses c
JOIN sports s ON c.sport_id = s.sport_id
LEFT JOIN enrollments e ON c.course_id = e.course_id
                        AND e.enroll_month = %s
ORDER BY c.course_id
"""

NAME_SQL = """
SELECT member_id
FROM members 
WHERE name = %s
"""

FEE_SQL = """
SELECT DISTINCT course_id, course_name, fee
FROM courses
WHERE course_name = %s 
"""



# 수강 신청가능 목록 조회
def list_courses(conn):
    for c in conn.execute(LIST_SQL, (MONTH,)):
        print(f"{c['course_id']:>3} | {c['sport_name']} | {c['course_name']} | {c['class_days']} | {c['fee']:,}원")



COURSE_ID = 1

   
# 이름 조회 
def list_name(conn, name):
    for m in conn.execute(NAME_SQL, (name,)):
        print({m['member_id']}, {m['name']})


# 수강 신청
def enroll(conn, member_id, course_id):
    # TODO: 신청한 강좌의 수강료 추출
    fee = 0

    conn.execute(
        "INSERT INTO enrollments (member_id, course_id, enroll_month, status, pay_amount) "
        "VALUES (%s, %s, %s, '수강중', %s)",
        (member_id, course_id, MONTH, fee)
    )
    print("수강신청 완료되었습니다.")


# =====================================================================
def main():
    with psycopg.connect(DSN, row_factory=dict_row) as conn:
        # 사용자 이름 입력 
        user_name = input("이름: ").strip()
        # 사용자 회원을 MEMER_ID에 저장 
        MEMBER_ID = list_name(conn, user_name)

        # 수강 목록
        list_courses(conn)

        # 수강 신청
        enroll(conn, MEMBER_ID, COURSE_ID)



if __name__ == "__main__":
    main()