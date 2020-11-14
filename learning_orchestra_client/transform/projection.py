"""

"""
from response_treat import ResponseTreat
from dataset.dataset import Dataset
import requests
import time


class Projection:
    def __init__(self, ip_from_cluster):
        self.cluster_url = "http://" + ip_from_cluster + "/api/learningOrchestra/v1/transform/projection"

    # def delete_dataset_attributes_sync(self):

    # def insert_dataset_attributes_sync(self):

    # def insert_dataset_attribute_sync(self):

    # def reduce_dataset_sync(self):

    # def enlarge_dataset_sync(self):

    # def join_datasets_sync(self):

    # def join_dataset_sync(self):

    # def update_dataset_values_sync(self):

    def search_projections(self, projection_name, pretty_response=False):
        """
        description:  This method is responsible for retrieving a specific projection

        pretty_response: If true return indented string, else return dict.
        dataset_name: Is the name of the dataset file.
        limit: Number of rows to return in pagination(default: 10) (maximum is set at 20 rows per request)
        skip: Number of rows to skip in pagination(default: 0)

        return: Specific projection metadata stored in Learning Orchestra or an error if there is no such projections.
        """
        response = self.search_projections_content(projection_name, limit=1, pretty_response=pretty_response)
        return response

    def search_all_projections(self, pretty_response=False):
        """
        description: This method retrieves all projection metadata, it does not retrieve the projection content.

        pretty_response: If true return indented string, else return dict.

        return: All projections metadata stored in Learning Orchestra or an empty result.
        """
        cluster_url_projection = self.cluster_url
        response = requests.get(cluster_url_projection)
        return ResponseTreat().treatment(response, pretty_response)

    def search_projections_content(self, projection_name, query="{}", limit=0, skip=0, pretty_response=True):
        """
        description: This method is responsible for retrieving the dataset content

        pretty_response: If true return indented string, else return dict.
        dataset_name: Is the name of the dataset file.
        query: Query to make in MongoDB(default: empty query)
        limit: Number of rows to return in pagination(default: 10) (maximum is set at 20 rows per request)
        skip: Number of rows to skip in pagination(default: 0)

        return A page with some tuples or registers inside or an error if there is no such dataset. The current page
        is also returned to be used in future content requests.
        """
        cluster_url_projection = self.cluster_url + "/" + projection_name + "?query=" + query + "&limit=" + str(
            limit) + "&skip=" + str(skip)
        response = requests.get(cluster_url_projection)
        return ResponseTreat().treatment(response, pretty_response)

    def delete_projections(self, projection_name, pretty_response=False):
        """
        description: This method is responsible for deleting the projection. The delete operation is always synchronous
        because it is very fast, since the deletion is performed in background. If a projection was used by another task
        (Ex. histogram, pca, tuning and so forth), it cannot be deleted.

        pretty_response: If true return indented string, else return dict.
        projection_name: Represents the projection name.

        return: JSON object with an error message, a warning message or a correct delete message
        """
        cluster_url_projection = self.cluster_url + "/" + projection_name
        response = requests.delete(cluster_url_projection)
        return ResponseTreat().treatment(response, pretty_response)

    def its_ready(self, projection_name, pretty_response=True):
        """
        description: This method check from time to time using Time lib, if a projection has finished being inserted
        into the Learning Orchestra storage mechanism.

        pretty_response: If true return indented string, else return dict.
        """
        if pretty_response:
            print("\n---------- WAITING " + projection_name + " FINISH ----------")
        while True:
            time.sleep(self.WAIT_TIME)
            response = self.search_projections_content(projection_name, limit=1, pretty_response=False)
            if len(response["result"]) == 0:
                continue
            if response["result"][self.METADATA_INDEX]["finished"]:
                break

    def insert_dataset_attributes_async(self, dataset_name, projection_name, fields, pretty_response=False):
        """
        description: This method inserts a set of attributes into a dataset. It can create a new dataset or reuse the
        existing one.

        pretty_response: If true return indented string, else return dict.
        datasetName: Represents the dataset name.
        fields: Represents the set of attributes to be inserted.

        return: A JSON object with error or warning messages. In case of success, it returns the dataset metadata.
        """
        if pretty_response:
            print(
                "\n----------"
                + " CREATE PROJECTION FROM "
                + dataset_name
                + " TO "
                + projection_name
                + " ----------"
            )
        request_body = {
            "inputDatasetName": dataset_name,
            "outputDatasetName": projection_name,
            "names": fields,
        }
        Dataset.its_ready(dataset_name, pretty_response)
        request_url = self.cluster_url
        response = requests.post(url=request_url, json=request_body)
        return ResponseTreat().treatment(response, pretty_response)




