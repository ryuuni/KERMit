import Header from '../../components/Header';

const PageTemplate = ({ children }) => {
  return (
    <>
      <Header />
      <div>
        {children}
      </div>
    </>
  );
};

export default PageTemplate;