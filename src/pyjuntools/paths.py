import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Union

class ProjectPaths:
    def __init__(self):
        self.base_path = ""
        
    def get_base_path(self, project_name: str) -> Path:
        """
        Find the first existing directory from a list of possible project directories
        and return the full path for the specified project.
        
        Args:
            project_name: Name of the project
            
        Returns:
            Path object representing the project's base directory
        """
        directories = [
            "/Users/jun/Dropbox/science/projects/",  # nagaimo
            "/Volumes/Carrot/Dropbox/science/projects/",  # ricotta
            "/home/ubuntu/science/projects/",  # aws
            "/pub/jallard/science/projects/",  # hpc3
            ".",  # if none of the above are found, default to current directory
        ]
        
        # Find first existing directory
        self.base_path = next(
            (dir for dir in directories if os.path.isdir(dir)),
            "."  # Default to current directory if none found
        )
        
        return Path(self.base_path) / project_name
    
    def get_path(self, 
                 project_name: str, 
                 subfolder: str, 
                 date: Optional[Union[str, datetime]] = None) -> Path:
        """
        Get path to a dated subfolder within a project, creating it if it doesn't exist.
        
        Args:
            project_name: Name of the project
            subfolder: Name of the subfolder (e.g., 'data', 'plots')
            date: Optional date string (YYMMDD) or datetime object. Defaults to today.
            
        Returns:
            Path object representing the dated subfolder
        """
        if date is None:
            date = datetime.now().strftime("%y%m%d")
        elif isinstance(date, datetime):
            date = date.strftime("%y%m%d")
            
        path = self.get_base_path(project_name) / subfolder / str(date)
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    def get_plot_path(self, 
                      project_name: str, 
                      date: Optional[Union[str, datetime]] = None) -> Path:
        """Get path to the plots folder for a given date."""
        return self.get_path(project_name, "plots", date)
    
    def get_data_path(self, 
                      project_name: str, 
                      date: Optional[Union[str, datetime]] = None) -> Path:
        """Get path to the data folder for a given date."""
        return self.get_path(project_name, "data", date)


# Create a singleton instance
paths = ProjectPaths()

# Example usage:
if __name__ == "__main__":
    run_name = "bubblegum"
    project = "TCRPulsing"
    
    base_path = paths.get_base_path(project)
    data_path = paths.get_data_path(project)
    
    # Example of saving data
    this_run_description = f"{run_name}_something"
    save_path = data_path / f"{this_run_description}.pkl"
    
    print(f"Base path: {base_path}")
    print(f"Data path: {data_path}")
    print(f"Save path: {save_path}")
