from uuid import uuid4

from build_task_manager.tasks.task_storage import Task, TaskStorage


class DependencyNotFoundError(Exception):
    def __init__(self, dependency_name: str):
        self.dependency = dependency_name


class DependencyCycleFinder:
    def __init__(self, build_tasks: list[str], tasks: TaskStorage):
        self.build_tasks = build_tasks
        self.tasks = tasks.get_all_tasks()
        self.build_task_name = str(uuid4())

    def find_cycle(self):
        self.visited = set()
        self.recursion_path_stack = []
        self.recursion_path_set = set()
        # This is so we don't have to deal with a forest - it's a single tree now
        self.tasks[self.build_task_name] = Task(
            name=self.build_task_name, dependencies=self.build_tasks
        )
        self.cycle = []
        self.cycle_finished = False
        self._dfs(self.build_task_name)
        del self.tasks[self.build_task_name]
        self.visited.remove(self.build_task_name)
        if self.cycle_finished:
            return self.cycle
        return None

    def get_dependencies(self) -> set[str]:
        return self.visited

    def _dfs(self, task_name: str):
        self.visited.add(task_name)
        self.recursion_path_stack.append(task_name)
        self.recursion_path_set.add(task_name)
        if task_name not in self.tasks:
            raise DependencyNotFoundError(task_name)
        for dependency in self.tasks[task_name].dependencies:
            if dependency in self.recursion_path_set:
                self.cycle.append(dependency)
                return True
            if self._dfs(dependency):
                if not self.cycle_finished:
                    task = self.recursion_path_stack.pop()
                    self.cycle.append(task)
                    if task == self.cycle[0]:
                        self.cycle_finished = True
                return True
        self.recursion_path_set.remove(self.recursion_path_stack.pop())
        return False
