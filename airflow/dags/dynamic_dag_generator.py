from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import pendulum
import random
import requests
import json

print("Starting DAG generation script...")

def create_dag(simulator_id, start_date, interval, kpi_id):
    print(f"Creating DAG for simulator {simulator_id}")
    
    dag_id = f'simulator_dag_{simulator_id}'

    def generate_and_process_value(**context):
        """
        Task to generate random value and calculate KPI
        """
        try:
            current_time = pendulum.now('UTC')
            # Generate random value
            value = random.uniform(1, 100)
            print(f"\n{'='*50}")
            print(f"Execution Time: {current_time}")
            print(f"Generated Value: {value}")
            
            # Calculate KPI
            calc_query = """
            query($kpiId: Int!, $value: Float!) {
                calculateKpi(kpiId: $kpiId, value: $value)
            }
            """
            
            calc_variables = {
                'kpiId': int(kpi_id),
                'value': float(value)
            }
            
            # Make KPI calculation request
            calc_response = requests.post(
                'http://web:8000/graphql/',
                json={
                    'query': calc_query,
                    'variables': calc_variables
                },
                headers={
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                timeout=10
            )
            
            print(f"KPI Calculation Response: {calc_response.text}")
            
            if calc_response.status_code == 200:
                calc_result = calc_response.json()
                if 'errors' in calc_result:
                    raise Exception(f"GraphQL errors in KPI calculation: {calc_result['errors']}")
                
                calculated_value = calc_result['data']['calculateKpi']
                print(f"Calculated KPI Value: {calculated_value}")
                next_run = current_time.add(seconds=interval)
                print(f"Next run scheduled at: {next_run}")
                print(f"{'='*50}\n")
                return calculated_value
            else:
                raise Exception(f"HTTP {calc_response.status_code}: {calc_response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"Request error: {str(e)}")
            raise
        except Exception as e:
            print(f"Error in task: {str(e)}")
            raise

    default_args = {
        'owner': 'airflow',
        'depends_on_past': False,
        'start_date': start_date,
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 3,
        'retry_delay': timedelta(seconds=5),  # Changed to seconds
    }

    # Using timedelta for seconds-based scheduling
    dag = DAG(
        dag_id=dag_id,
        default_args=default_args,
        schedule_interval=timedelta(seconds=interval),  # Changed to timedelta
        catchup=False,
        tags=['simulator']
    )
    dag.timezone = pendulum.timezone('UTC')

    with dag:
        task = PythonOperator(
            task_id='generate_and_process_value',
            python_callable=generate_and_process_value,
            provide_context=True,
            retries=3,
            retry_delay=timedelta(seconds=5)  # Changed to seconds
        )

    return dag

# Get simulators and create DAGs
try:
    print("Fetching simulators from Django...")
    response = requests.post(
        'http://web:8000/graphql/',
        json={
            'query': '''
                query {
                    simulators {
                        id
                        startDate
                        interval
                        kpiId {
                            id
                        }
                    }
                }
            '''
        },
        headers={'Content-Type': 'application/json'}
    )
    
    data = response.json()
    simulators = data['data']['simulators']
    print(f"Found {len(simulators)} simulators")

    for simulator in simulators:
        try:
            dag_id = f'simulator_dag_{simulator["id"]}'
            start_date = pendulum.parse(simulator['startDate']).in_timezone('UTC')
            
            print(f"Creating DAG: {dag_id}")
            print(f"Interval: {simulator['interval']} seconds")
            
            globals()[dag_id] = create_dag(
                simulator_id=simulator['id'],
                start_date=start_date,
                interval=simulator['interval'],
                kpi_id=simulator['kpiId']['id']
            )
            print(f"Created DAG: {dag_id}")
        except Exception as e:
            print(f"Error creating DAG for simulator {simulator['id']}: {e}")

except Exception as e:
    print(f"Error fetching simulators: {e}")

print("DAG generation script completed")