from setuptools import setup, find_packages

setup(
    name='aws-course-recommendation-ai',
    version='1.0.0',
    description='AWS Course Recommendation AI System with multi-agent architecture',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[
        'boto3>=1.34.0',
        'requests>=2.31.0',
        'beautifulsoup4>=4.12.0',
        'pandas>=2.0.0',
        'aiohttp>=3.8.0',
        'scikit-learn>=1.3.0',
        'numpy>=1.24.0',
        'asyncio-throttle>=1.0.0',
        'python-dotenv>=1.0.0',
        'pydantic>=2.0.0',
        'fastapi>=0.100.0',
        'uvicorn>=0.23.0',
    ],
    python_requires='>=3.9',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
