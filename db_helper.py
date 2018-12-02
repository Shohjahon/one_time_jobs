import sqlite3


def create_table():
    conn = sqlite3.connect('jobs.sqlite')
    cursor = conn.cursor()

    query = '''
    CREATE TABLE IF NOT EXISTS one_time_jobs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_name TEXT,
    job_about TEXT,
    job_category TEXT,
    job_price TEXT,
    job_date TEXT,
    job_owner_phone TEXT,
    job_address TEXT,
    coordinate TEXT
    )
    '''
    cursor.execute(query)
    conn.commit()
    conn.close()


def add_spot(job_name, job_about, job_category, job_price, job_date, job_owner_phone, job_address, coordinate):
    conn = sqlite3.connect('jobs.sqlite')
    cursor = conn.cursor()

    query = '''
    INSERT INTO one_time_jobs(job_name, job_about, job_category, job_price, job_date, job_owner_phone, job_address, coordinate)
    VALUES(?,?,?,?,?,?,?,?)
    '''
    cursor.execute(query, (job_name, job_about, job_category, job_price, job_date, job_owner_phone, job_address, coordinate))
    conn.commit()
    conn.close()


def get_spots():
    conn = sqlite3.connect('jobs.sqlite')

    cursor = conn.cursor()

    query = '''
	    SELECT *
	    FROM one_time_jobs
	'''

    cursor.execute(query)
    all_rows = cursor.fetchall()

    conn.commit()
    conn.close()

    return all_rows


def get_spot_by_type(type):
    conn = sqlite3.connect('jobs.sqlite')

    cursor = conn.cursor()

    query = '''
	    SELECT *
	    FROM one_time_jobs
	    WHERE job_type = '{}';
	'''.format(type)

    cursor.execute(query)
    all_rows = cursor.fetchall()

    conn.commit()
    conn.close()

    return all_rows


def update_spot(id, spot_name, address, phone_number, working_hours, coordination, spot_type):
    conn = sqlite3.connect('jobs.sqlite')

    cursor = conn.cursor()

    query = '''
	    UPDATE tourist_spots
	    SET spot_name=?,address=?,phone_number=?,working_hours=?,coordination=?,spot_type=?
	    WHERE id = ?
	'''

    cursor.execute(query, (id, spot_name, address, phone_number, working_hours, coordination, spot_type))

    conn.commit()
    conn.close()


def delete_spot(id):
    conn = sqlite3.connect('jobs.sqlite')

    cursor = conn.cursor()

    query = '''
	    DELETE
	    FROM one_time_jobs
	    WHERE id = {}
	'''.format(id)

    cursor.execute(query)
    all_rows = cursor.fetchall()

    conn.commit()
    conn.close()

    return all_rows


def get_spot_by_name(name):
    conn = sqlite3.connect('jobs.sqlite')

    cursor = conn.cursor()

    query = '''
    	    SELECT *
    	    FROM one_time_jobs
    	    WHERE job_name like '{}';
    	'''.format(name)

    cursor.execute(query)
    all_rows = cursor.fetchall()

    conn.commit()
    conn.close()

    return all_rows


def getByRegionDistrict(region, district):
    jobs = get_spots()
    job_list = []
    for job in jobs:
        address = job[7]
        temp = str(address).split(',')

        if len(temp) >= 2 :
            reg = temp[0]
            dist = temp[1]
            if region == reg and dist == district:
                print(job)
                job_list.append(job)

    return job_list


#if __name__ == '__main__':
    #add_spot('sdf','sdf','sdf','sdf','sdf','sdf','sdf','sdf')
    #print(getByRegionDistrict('Tashkent', ))


